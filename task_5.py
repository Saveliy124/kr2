from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
import uuid
import time
import hmac
import hashlib

app = FastAPI(title="Задания 5.1 - 5.3")

SECRET_KEY = "super_secret_key_for_hmac"

class LoginData(BaseModel):
    username: str
    password: str

def create_signature(user_id: str, timestamp: str) -> str:
    """Генерация HMAC подписи."""
    msg = f"{user_id}.{timestamp}".encode('utf-8')
    return hmac.new(SECRET_KEY.encode(), msg, hashlib.sha256).hexdigest()

@app.post("/login")
def login(data: LoginData, response: Response):
    if data.username != "user123" or data.password != "password123":
        response.status_code = 401
        return {"message": "Unauthorized"}
    
    user_id = str(uuid.uuid4())
    timestamp = str(int(time.time()))
    signature = create_signature(user_id, timestamp)
    
    cookie_value = f"{user_id}.{timestamp}.{signature}"
    response.set_cookie(
        key="session_token", 
        value=cookie_value, 
        httponly=True, 
        secure=False,  
        max_age=300    
    )
    return {"message": "Logged in successfully"}

@app.get("/profile")
def profile(request: Request, response: Response):
    token = request.cookies.get("session_token")
    if not token:
        response.status_code = 401
        return {"message": "Unauthorized"}
    
    parts = token.split(".")
    if len(parts) != 3:
        response.status_code = 401
        return {"message": "Invalid session"}
        
    user_id, timestamp_str, signature = parts
    
    expected_sig = create_signature(user_id, timestamp_str)
    if not hmac.compare_digest(expected_sig, signature):
        response.status_code = 401
        return {"message": "Invalid session"}
    
    try:
        last_active = int(timestamp_str)
    except ValueError:
        response.status_code = 401
        return {"message": "Invalid session"}
        
    current_time = int(time.time())
    elapsed = current_time - last_active
    
    if elapsed >= 300: 
        response.status_code = 401
        return {"message": "Session expired"}
    
    if elapsed >= 180: 
        new_timestamp = str(current_time)
        new_signature = create_signature(user_id, new_timestamp)
        new_cookie = f"{user_id}.{new_timestamp}.{new_signature}"
        response.set_cookie(
            key="session_token", 
            value=new_cookie, 
            httponly=True, 
            secure=False, 
            max_age=300
        )
        
    return {"user_id": user_id, "profile_data": "Секретные данные пользователя"}