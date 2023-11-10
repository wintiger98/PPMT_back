from fastapi import APIRouter, HTTPException, Depends, Form
from ..database import get_db
from ..schemas.project_schemas import (
    ProjectContentInput,
    ProjectContentOutput,
    ProjectInput,
    ProjectOutput,
    ProjectOneOutput,
)
from sqlalchemy.orm import Session
from typing import List

from ..crud.crud_project import (
    create_project,
    delete_project,
    get_project_by_user_id,
    get_project,
    update_project,
    change_project_fit_with_schema,
)

from ..crud.crud_auth import get_current_user_email, get_user_by_email


router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)


@router.post("", response_model=ProjectOutput)
async def make_project(
    data: ProjectInput,
    email: str = Depends(get_current_user_email),
    db: Session = Depends(get_db),
):
    """## Args

    | Parameter | Type | Description |
    | --------- | ---- | ----------- |
    | data | ProjectInput |  |


    ## Returns

    | Type | Description |
    | ---- | ----------- |
    | _type_ | ProjectOutput |
    """
    user = get_user_by_email(email=email, db=db)
    if not user:
        raise HTTPException(status_code=400, detail="Not User found")
    data = data.model_dump()
    data["user_id"] = user.id
    project = create_project(data=data, db=db)
    project = change_project_fit_with_schema(project=project)

    return project


@router.get("", response_model=List[ProjectOutput])
async def get_projects(
    email: str = Depends(get_current_user_email), db: Session = Depends(get_db)
):
    """다수의 project 조회

    Args:
        user_id (int): user의 pk
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: _description_

    Returns:
        List: List[ProjectOutput]
    """
    user = get_user_by_email(email=email, db=db)
    if not user:
        raise HTTPException(status_code=400, detail="Not User found")
    projects = get_project_by_user_id(user_id=user.id, db=db)
    if projects is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return projects


@router.get("/{project_id}", response_model=ProjectOneOutput)
async def get_one_project(project_id: int, db: Session = Depends(get_db)):
    """project_id로 단일 project 조회

    Args:
        project_id (int): project pk
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: _description_

    Returns:
        dict: ProjectOutput
    """
    project = get_project(project_id=project_id, db=db)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    project = change_project_fit_with_schema(project=project)
    return project


@router.put("/{project_id}", response_model=ProjectOutput)
async def change_project(
    project_id: int, data: ProjectInput, db: Session = Depends(get_db)
):
    """project 수정

    Args:
        project_id (int): project pk
        data (ProjectInput): ProjectInput
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: _description_

    Returns:
        _type_: ProjectOutput
    """
    project = update_project(project_id=project_id, data=data.model_dump(), db=db)
    if not project:
        raise HTTPException(status_code=400, detail="Update failed")
    project = change_project_fit_with_schema(project=project)
    return project


@router.delete("/{project_id}", response_model=dict)
async def erase_user(project_id: int, db: Session = Depends(get_db)):
    """project 삭제

    Args:
        project_id (int): project pk
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: _description_

    Returns:
        _type_: dict 성공시 {"success" : True}
    """
    success = delete_project(project_id=project_id, db=db)
    if not success:
        raise HTTPException(status_code=400, detail="Delete failed")
    return {"success": True}
