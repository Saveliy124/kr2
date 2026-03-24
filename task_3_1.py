from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

app = FastAPI(title="Задание 3.1")

class UserCreate(BaseModel):
    name: str 
    email: EmailStr 
    age: Optional[int] = Field(default=None, gt=0) 
    is_subscribed: Optional[bool] = False 

@app.post("/create_user")
def create_user(user: UserCreate):
    
    return user