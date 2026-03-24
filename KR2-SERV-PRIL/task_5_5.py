from fastapi import FastAPI, Header, HTTPException, Depends, Response
from pydantic import BaseModel, field_validator
from datetime import datetime
import re

app = FastAPI(title="Задание 5.5")

# 1. Модель Pydantic для валидации заголовков
class CommonHeaders(BaseModel):
    user_agent: str
    accept_language: str

    @field_validator("accept_language")
    def validate_language(cls, v):
        # Проверка формата заголовка Accept-Language
        if not re.match(r"^[a-zA-Z0-9\-\,\;\=\.\s]+$", v):
            raise ValueError("Неверный формат заголовка Accept-Language")
        return v

# Функция-зависимость для сборки модели из заголовков FastAPI
def get_common_headers(
    user_agent: str = Header(..., alias="User-Agent"),
    accept_language: str = Header(..., alias="Accept-Language")
):
    try:
        return CommonHeaders(user_agent=user_agent, accept_language=accept_language)
    except ValueError as e:
        # Если Pydantic выбросит ValueError из-за формата, возвращаем 400
        raise HTTPException(status_code=400, detail=str(e))

# 2. Маршрут /headers (использует модель)
@app.get("/headers")
def get_headers_route(headers: CommonHeaders = Depends(get_common_headers)):
    return {
        "User-Agent": headers.user_agent,
        "Accept-Language": headers.accept_language
    }

# 3. Маршрут /info (использует модель + добавляет заголовок в ответ)
@app.get("/info")
def get_info_route(response: Response, headers: CommonHeaders = Depends(get_common_headers)):
    # Добавляем серверное время в заголовки ответа
    response.headers["X-Server-Time"] = datetime.now().isoformat()
    
    return {
        "message": "Добро пожаловать! Ваши заголовки успешно обработаны.",
        "headers": {
            "User-Agent": headers.user_agent,
            "Accept-Language": headers.accept_language
        }
    }