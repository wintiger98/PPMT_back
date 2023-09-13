from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    password: str


class UserOutput(UserBase):
    created_at: Optional[datetime]
