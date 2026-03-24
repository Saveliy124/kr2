from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

app = FastAPI(title="Задание 3.1")

# Модель для представления данных пользователя
class UserCreate(BaseModel):
    name: str # Имя пользователя (обязательно)
    email: EmailStr # Email должен иметь допустимый формат
    age: Optional[int] = Field(default=None, gt=0) # Возраст должен быть > 0
    is_subscribed: Optional[bool] = False # Флажок подписки

@app.post("/create_user")
def create_user(user: UserCreate):
    # Возвращаем полученную пользовательскую информацию
    return user