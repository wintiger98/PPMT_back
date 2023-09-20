from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ProjectBase(BaseModel):
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    tech: Optional[list[str]] = None
    title: Optional[str] = None
    categories: Optional[list[str]] = None


class ProjectOutput(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime


class ProjectInput(ProjectBase):
    pass
