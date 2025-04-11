from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    PROJECT_NAME: str = "Marketplace Blog"
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/dbname"
    JWT_SECRET_KEY: str = "your-secret-key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    celery_broker_url: str = "amqp://guest:guest@localhost:5672//"

    smtp_server: str
    smtp_port: int
    smtp_user: str
    smtp_password: str

    # настройки типа s3 (minio)
    minio_endpoint: str
    minio_access_key: str
    minio_secret_key: str
    minio_bucket: str

    class Config:
        env_file = ".env"

settings = Settings()
