from pydantic import BaseModel

# Схема для создания категории
class CategoryCreate(BaseModel):
    name: str

# Схема для обновления категории (при необходимости)
class CategoryUpdate(BaseModel):
    name: str

# Схема для ответа
class CategoryOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True # чтоб потом можно было конвертировать объекты SQLAlchemy в Pydantic
