# app/models/association.py
from sqlalchemy import Table, Column, Integer, ForeignKey
from app.db.base import Base


#связка многие ко многим
article_category = Table(
    'article_category',
    Base.metadata,
    Column('article_id', Integer, ForeignKey('articles.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
)
