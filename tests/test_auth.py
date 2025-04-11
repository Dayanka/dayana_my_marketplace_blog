import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.base import Base
from app.api.v1.dependencies import get_db


#  тестовая SQLite бд для тестов
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#  тестовая база
Base.metadata.create_all(bind=engine)

# переопределяем зависимость get_db для тестов
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_register_and_login():
    # регаем юзера
    register_data = {"email": "testuser@example.com", "password": "testpassword"}
    response = client.post("/auth/register", json=register_data)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "user_id" in data

    # логинюсь и получаю токен
    login_data = {"username": "testuser@example.com", "password": "testpassword"}
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    return data["access_token"]


def test_upload_image(tmp_path):
    # токен для аутентификации
    token = test_register_and_login()

    # временный файл для теста загрузки? хз правильно ли
    d = tmp_path / "sub"
    d.mkdir()
    file_path = d / "image.jpg"
    file_path.write_bytes(b"Test image content")

    # отправляю запрос на загрузку
    with open(file_path, "rb") as file_obj:
        response = client.post(
            "/images/",
            headers={"Authorization": f"Bearer {token}"},
            files={"file": ("image.jpg", file_obj, "image/jpeg")},
        )
    # проверка успеха
    assert response.status_code == 200, response.text
    data = response.json()
    assert "url" in data
