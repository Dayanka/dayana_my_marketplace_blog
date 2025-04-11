import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.api.v1.dependencies import get_db



SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.drop_all(bind=engine)  # очищаем перед запуском
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# тесты аутентификации
def test_register_and_login():
    # регаем юзера
    register_data = {"email": "article_user@example.com", "password": "password123"}
    response = client.post("/auth/register", json=register_data)
    assert response.status_code == 200, f"Register failed: {response.text}"

    # Логинюсь
    login_data = {"username": "article_user@example.com", "password": "password123"}
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200, f"Login failed: {response.text}"
    data = response.json()
    assert "access_token" in data
    token = data["access_token"]
    return token

# тест на создание категории
def test_create_category():
    category_data = {"name": "технологии"}
    response = client.post("/categories/", json=category_data)
    assert response.status_code == 200, f"Create category failed: {response.text}"
    data = response.json()
    assert "id" in data, f"Category id not found in response: {data}"
    return data["id"]

# тест на получение категорий
def test_get_categories():
    response = client.get("/categories/")
    assert response.status_code == 200, f"Get categories failed: {response.text}"
    data = response.json()
    assert isinstance(data, list), f"Expected list, got {type(data)}"
    return data

# тест создания статьи с привязкой категории
def test_create_article_with_category():
    token = test_register_and_login()
    # создаю категорию
    category_data = {"name": "наука"}
    category_response = client.post("/categories/", json=category_data)
    assert category_response.status_code == 200, f"Category creation failed: {category_response.text}"
    category_id = category_response.json()["id"]

    # создаем статью, передаю category_ids
    article_data = {
        "title": "Заголовок статьи",
        "summary": "Краткое описание",
        "content": "Полный текст статьи",
        "category_ids": [category_id]
    }
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/articles/", json=article_data, headers=headers)
    assert response.status_code == 200, f"Article creation failed: {response.text}"
    data = response.json()
    assert data["title"] == "Заголовок статьи", f"Unexpected title: {data['title']}"
    # проверка, что категория привязана
    assert "categories" in data and isinstance(data["categories"], list), "Categories missing in response"
    assert len(data["categories"]) == 1, f"Expected 1 category, got {len(data['categories'])}"
    assert data["categories"][0]["id"] == category_id, "Category id does not match"
    return data["id"], token, category_id

# тест обновления статьи (изменения категории)
def test_update_article_category():
    article_id, token, _ = test_create_article_with_category()
    # создаем новую категорию для обновления
    new_category_data = {"name": "искусство"}
    response = client.post("/categories/", json=new_category_data)
    assert response.status_code == 200, f"New category creation failed: {response.text}"
    new_category_id = response.json()["id"]

    # обновляем статью - меняем title и категорию
    update_data = {
        "title": "Новый заголовок",
        "category_ids": [new_category_id]
    }
    headers = {"Authorization": f"Bearer {token}"}
    response = client.put(f"/articles/{article_id}", json=update_data, headers=headers)
    assert response.status_code == 200, f"Article update failed: {response.text}"
    data = response.json()
    assert data["title"] == "Новый заголовок", "Title was not updated"
    # проверяем, что категория изменилась
    assert len(data["categories"]) == 1, f"Expected 1 category, got {len(data['categories'])}"
    assert data["categories"][0]["id"] == new_category_id, "Updated category does not match"
    return article_id, token

# сест мягкого удаления статьи
def test_soft_delete_article():
    article_id, token, _ = test_create_article_with_category()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete(f"/articles/{article_id}", headers=headers)
    assert response.status_code == 200, f"Article deletion failed: {response.text}"
    data = response.json()
    assert "Article soft-deleted" in data["message"], f"Unexpected deletion message: {data}"
    # после удаления, попытка получить статью должна вернуть 404
    response = client.get(f"/articles/{article_id}")
    assert response.status_code == 404, "Deleted article was found"
