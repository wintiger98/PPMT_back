from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    user_name: str
    password: str


class UserOutput(UserBase):
    created_at: Optional[datetime]
