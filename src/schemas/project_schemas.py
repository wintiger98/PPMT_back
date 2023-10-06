from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ProjectContentBase(BaseModel):
    order: int
    title: str
    imageUrl: Optional[str]
    contents: Optional[str]


class ProjectContentOutput(ProjectContentBase):
    id: int


class ProjectBase(BaseModel):
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    tech: Optional[list[str]] = None
    title: Optional[str] = None
    categories: Optional[list[str]] = None
    description: Optional[str] = None


class ProjectOutput(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime


class ProjectOneOutput(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime
    project_contents: Optional[list[ProjectContentOutput]]


class ProjectInput(ProjectBase):
    pass
