from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.association import article_category



class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    # обратное отношение к статьям
    articles = relationship(
        "Article",
        secondary=article_category,
        back_populates="categories"
    )