from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ProjectContentBase(BaseModel):
    order: int
    title: Optional[str]
    imageUrl: Optional[str]
    contents: Optional[str]


class ProjectContentOutput(ProjectContentBase):
    pass


class ProjectContentInput(ProjectContentBase):
    id: int
    project_id: int
