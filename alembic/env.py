import sys
import os
from app.models import user, article, category

# Добавляем корневую папку проекта в sys.path, чтобы можно было импортировать наши модули
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from alembic import context
config = context.config

# Импортируем настройки и базовую модель
from app.config import settings
from app.db.base import Base
# Импортируем модели, чтобы они регистрировались в Base.metadata
from app.models import user, article, category

# Указываем, что metadata берется из Base
target_metadata = Base.metadata

# Устанавливаем URL для подключения к базе данных из наших настроек
config.set_main_option('sqlalchemy.url', settings.DATABASE_URL)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True  # Добавлено для сравнения типов
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    from sqlalchemy import engine_from_config, pool
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True  # Добавлено для обнаружения изменений в типах столбцов
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
