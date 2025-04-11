# app/db/base.py
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Импортируем модели, чтобы они зарегистрировались в Base.metadata
from app.models import user, article, category


