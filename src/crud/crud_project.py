from typing import List
from ..models import Project, ProjectContent
from sqlalchemy import desc, select, delete, update, and_
from sqlalchemy.orm import Session


def list2string(tmp_list):
    return ",".join(tmp_list)


def string2list(tmp_string):
    return tmp_string.split(",")


def change_project_fit_with_schema(project: Project):
    if project.tech:
        project.tech = string2list(project.tech)
    if project.categories:
        project.categories = string2list(project.categories)
    return project


def get_project_by_user_id(user_id: int, db: Session) -> List[Project]:
    stmt = (
        select(Project)
        .where(Project.user_id == user_id)
        .order_by(desc(Project.updated_at))
    )
    result = db.execute(stmt)
    projects = result.scalars().all()
    for project in projects:
        project = change_project_fit_with_schema(project)
    return projects


def get_project(project_id: int, db: Session) -> Project:
    stmt = select(Project).where(Project.id == project_id)
    result = db.execute(stmt)
    project = result.scalar()
    return project


def data_preprocess(data: dict):
    if data.get("tech"):
        data["tech"] = list2string(data["tech"])
    if data.get("categories"):
        data["categories"] = list2string(data["categories"])
    return data


def create_project(data: dict, db: Session) -> Project:
    data = data_preprocess(data=data)
    project = Project(**data)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

def update_project_contents(project, project_contents):
    contents = []
    for content in project_contents:
        tmp_content = ProjectContent()
        for key, value in content.items():
            setattr(tmp_content,key,value)
        contents.append(tmp_content)
    project.project_contents = contents
    return project

def update_project(project_id: int, data: dict, db: Session) -> Project:
    data = data_preprocess(data=data)
    stmt = select(Project).where(Project.id == project_id)
    result = db.execute(stmt)
    project = result.scalar()

    for key, value in data.items():
        if key == "user_id" or key == "id":
            continue
        if key == "project_contents":
            project = update_project_contents(project=project, project_contents=value)
            continue
        setattr(project, key, value)

    db.commit()
    db.refresh(project)

    return project


def delete_project(project_id: int, db: Session):
    stmt = delete(Project).where(Project.id == project_id)
    db.execute(stmt)
    db.commit()
    return True
