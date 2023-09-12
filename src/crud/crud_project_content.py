from typing import List
from ..models import ProjectContent
from sqlalchemy import select, delete, update, and_
from sqlalchemy.orm import Session


def get_project_content_by_project_id(
    project_id: int, db: Session
) -> List[ProjectContent]:
    stmt = select(ProjectContent).where(ProjectContent.project_id == project_id)
    result = db.execute(stmt)
    project_contents = result.scalars().all()
    return project_contents


def get_project_content(project_content_id: int, db: Session) -> ProjectContent:
    stmt = select(ProjectContent).where(ProjectContent.id == project_content_id)
    result = db.execute(stmt)
    project = result.scalar()
    return project


def create_project_content(data: dict, db: Session) -> ProjectContent:
    project_content = ProjectContent(**data)

    db.add(project_content)
    db.commit()
    db.refresh(project_content)
    return project_content


def update_project_content(
    project_content_id: int, data: dict, db: Session
) -> ProjectContent:
    stmt = select(ProjectContent).where(ProjectContent.id == project_content_id)
    result = db.execute(stmt)
    project_content = result.scalar()

    for key, value in data.items():
        setattr(project_content, key, value)

    db.commit()
    db.refresh(project_content)

    return project_content


def delete_project_content(project_content_id: int, db: Session):
    stmt = delete(ProjectContent).where(ProjectContent.id == project_content_id)
    db.execute(stmt)
    db.commit()
    return None
