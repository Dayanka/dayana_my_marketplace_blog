from fastapi import APIRouter, HTTPException, Depends
import sqlalchemy as sa
from sqlalchemy.orm import Session
from typing import List, Optional


from app.models.article import Article
from app.models.category import Category
from app.models.user import User
from app.schemas.article import ArticleCreate, ArticleUpdate, ArticleOut
from app.api.v1.dependencies import get_db, get_current_user


router = APIRouter(prefix="/articles", tags=["articles"])


# Создание новой статьи (только для авторизованных пользователей)
@router.post("/", response_model=ArticleOut)
def create_article(
        article: ArticleCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    db_article = Article(
        title=article.title,
        summary=article.summary,
        content=article.content
    )
    if article.category_ids:
        categories = db.query(Category).filter(Category.id.in_(article.category_ids)).all()
        if not categories:
            raise HTTPException(status_code=404, detail="Some categories not found")
        db_article.categories = categories

    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


# Получение списка статей
@router.get("/", response_model=List[ArticleOut])
def read_articles(
    page_number: int = 1,
    page_size: int = 10,
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    MAX_PAGE_SIZE = 50
    if page_size > MAX_PAGE_SIZE:
        page_size = MAX_PAGE_SIZE

    # только НЕ удалённые статьи
    query = db.query(Article).filter(Article.is_deleted == False)

    # полнотекстовый поиск (если search-параметр указан). поиск по объединённым полям title и content
    if search:
        query = query.filter(
            sa.func.to_tsvector('english', Article.title + ' ' + Article.content).match(search)
        )

    #фильтрация статей по конкретной категории
    #выполняется join с таблицей категорий
    if category_id:
        query = query.join(Article.categories).filter(Category.id == category_id)
    #пагинация с ограничением максимального размера страницы
    offset = (page_number - 1) * page_size
    articles = query.offset(offset).limit(page_size).all()
    return articles

# Получение конкретной статьи
@router.get("/{article_id}", response_model=ArticleOut)
def read_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id, Article.is_deleted == False).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


# Обновление статьи (только для авторизованных пользователей)
@router.put("/{article_id}", response_model=ArticleOut)
def update_article(
        article_id: int,
        article_update: ArticleUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    if article_update.title is not None:
        article.title = article_update.title
    if article_update.summary is not None:
        article.summary = article_update.summary
    if article_update.content is not None:
        article.content = article_update.content
    if article_update.category_ids is not None:
        categories = db.query(Category).filter(Category.id.in_(article_update.category_ids)).all()
        article.categories = categories

    db.commit()
    db.refresh(article)
    return article


# Удаление статьи - защищенный эндпоинт
@router.delete("/{article_id}")
def delete_article(
        article_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    # Мягкое удаление- просто обновляю флаг is_deleted
    article.is_deleted = True
    db.commit()
    db.refresh(article)
    return {"message": "Article soft-deleted", "article_id": article.id}
