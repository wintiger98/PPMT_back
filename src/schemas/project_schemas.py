from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from fastapi import UploadFile


class ProjectContentBase(BaseModel):
    # order: Optional[int]
    title: str
    link_url: Optional[str]
    contents: Optional[str]


class ProjectContentOutput(ProjectContentBase):
    id: int
    image_url: Optional[str]


class ProjectContentInput(ProjectContentBase):
    image: Optional[str] = ""
    image_url: Optional[str] = ""


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
    project_contents: Optional[list[ProjectContentInput]]
