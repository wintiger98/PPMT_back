from typing import List
from ..models import Project
from sqlalchemy import select, delete, update, and_
from sqlalchemy.orm import Session


def get_project_by_user_id(user_id: int, db: Session) -> List[Project]:
    stmt = select(Project).where(Project.user_id == user_id)
    result = db.execute(stmt)
    projects = result.scalars().all()
    return projects


def get_project(project_id: int, db: Session) -> Project:
    stmt = select(Project).where(Project.id == project_id)
    result = db.execute(stmt)
    project = result.scalar()
    return project


def create_project(data: dict, db: Session) -> Project:
    project = Project(**data)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def update_project(project_id: int, data: dict, db: Session) -> Project:
    stmt = select(Project).where(Project.id == project_id)
    result = db.execute(stmt)
    project = result.scalar()

    for key, value in data.items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)

    return project


def delete_project(project_id: int, db: Session):
    stmt = delete(Project).where(Project.id == project_id)
    db.execute(stmt)
    db.commit()
    return None
