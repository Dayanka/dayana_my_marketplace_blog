from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from app.schemas.category import CategoryOut

# Схема для создания статьи (входящие данные)
class ArticleCreate(BaseModel):
    title: str
    summary: Optional[str] = None
    content: str
    # Список ID категорий, к которым будет привязана статья
    category_ids: List[int] = []

# Схема для обновления статьи
class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    category_ids: Optional[List[int]] = None

# Схема для вывода статьи (выходные данные)
class ArticleOut(BaseModel):
    id: int
    title: str
    summary: Optional[str] = None
    content: str
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    categories: List[CategoryOut] = []

    class Config:
        orm_mode = True # чтоб корректно сериализовать объекты SQLAlchemy
