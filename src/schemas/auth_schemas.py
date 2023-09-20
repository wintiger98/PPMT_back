from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    password: str


class UserOutput(UserBase):
    id: int
    created_at: Optional[datetime]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
