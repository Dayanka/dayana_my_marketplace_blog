from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings



# движок (engine) подключения к бд
engine = create_engine(settings.DATABASE_URL, echo=True)

# фабрика сессий (sessionmaker)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

