from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ProjectBase(BaseModel):
    created_at: datetime
    updated_at: datetime
    start_at: datetime
    end_at: datetime
    tech: list[str]


class ProjectOutput(ProjectBase):
    pass


class ProjectInput(ProjectBase):
    pass
