from fastapi import FastAPI, Header, HTTPException
from typing import Optional
import re

app = FastAPI(title="Задание 5.4")

@app.get("/headers")
def get_headers(
    # Используем Header для извлечения заголовков.
    # Alias нужен, так как в Python нельзя использовать дефисы в именах переменных.
    user_agent: Optional[str] = Header(None, alias="User-Agent"),
    accept_language: Optional[str] = Header(None, alias="Accept-Language")
):
    # 1. Проверка на отсутствие заголовков
    if not user_agent or not accept_language:
        raise HTTPException(status_code=400, detail="Отсутствуют обязательные заголовки: User-Agent или Accept-Language")
    
    # 2. Опциональная проверка формата Accept-Language (с помощью регулярного выражения)
    if not re.match(r"^[a-zA-Z0-9\-\,\;\=\.\s]+$", accept_language):
        raise HTTPException(status_code=400, detail="Неверный формат заголовка Accept-Language")

    # 3. Возврат JSON-ответа
    return {
        "User-Agent": user_agent,
        "Accept-Language": accept_language
    }