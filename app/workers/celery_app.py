from celery import Celery
from app.config import settings
import os


#url брокера (rabbit)
# Получаем URL брокера из переменных окружения или используем значение по умолчанию
broker_url = os.getenv("CELERY_BROKER_URL", "amqp://guest:guest@localhost:5672//")

celery_app = Celery("worker", broker=broker_url)


# Настройка backend для хранения результатов
celery_app.conf.update(result_backend="rpc://")


# Импорт модуля задач, чтобы они были зарегистрированы
import app.workers.tasks