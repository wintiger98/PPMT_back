from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ProjectBase(BaseModel):
    start_at: Optional[datetime]
    end_at: Optional[datetime]
    tech: Optional[list[str]]
    title: Optional[str]
    categories: Optional[list[str]]


class ProjectOutput(ProjectBase):
    created_at: datetime
    updated_at: datetime
    pass


class ProjectInput(ProjectBase):
    pass
