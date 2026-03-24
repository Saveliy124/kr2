from fastapi import FastAPI, Header, HTTPException
from typing import Optional
import re

app = FastAPI(title="Задание 5.4")

@app.get("/headers")
def get_headers(
    user_agent: Optional[str] = Header(None, alias="User-Agent"),
    accept_language: Optional[str] = Header(None, alias="Accept-Language")
):
    if not user_agent or not accept_language:
        raise HTTPException(status_code=400, detail="Отсутствуют обязательные заголовки: User-Agent или Accept-Language")
    
    if not re.match(r"^[a-zA-Z0-9\-\,\;\=\.\s]+$", accept_language):
        raise HTTPException(status_code=400, detail="Неверный формат заголовка Accept-Language")

    return {
        "User-Agent": user_agent,
        "Accept-Language": accept_language
    }