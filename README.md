# dayana_my_marketplace_blog

# запустить тесты
docker-compose run --rm tests

# клонировать и запустить проект
git clone https://github.com/Dayanka/dayana_my_marketplace_blog.git

cd my_marketplace_blog

docker-compose build

docker-compose up


# Если нужно прогонять Alembic при каждом запуске app
command: >
  sh -c "poetry run alembic upgrade head &&
         poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000"

# 
Приложение  на http://127.0.0.1:8000

RabbitMQ на http://127.0.0.1:15672

Minio на http://127.0.0.1:9001 (логин/пароль: minioadmin)
