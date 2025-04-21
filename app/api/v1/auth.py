from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Optional
from pydantic import BaseModel
from passlib.context import CryptContext

from app.config import settings
from app.models.user import User
from app.api.v1.dependencies import get_db, get_current_user  # oauth2_scheme уже используется внутри get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pydantic схема для регистрации
class UserCreate(BaseModel):
    email: str
    password: str


#регистрация
@router.post("/register")
def register(user_data: UserCreate, db = Depends(get_db)):
    # Проверяем, существует ли уже пользователь с таким email
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already registered")
    # Шифруем пароль
    hashed_password = pwd_context.hash(user_data.password)
    # Создаем нового пользователя
    new_user = User(email=user_data.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    from app.workers.tasks import send_registration_email
    # асинхронно вызываем задачу отправки email (логирование, имитация)
    send_registration_email.delay(new_user.email)

    return {"message": "User registered successfully", "user_id": new_user.id}


#функция для создания jwt токена
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


#для логина
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_db)):
    # form_data.username будет содержать email пользователя
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}



#проверка
@router.get("/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return {"email": current_user.email}