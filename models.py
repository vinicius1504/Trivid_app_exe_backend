from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserIn(BaseModel):
    nome: str
    email: EmailStr
    idade: int

class UserOut(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    email: EmailStr
    age: int
