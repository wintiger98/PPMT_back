from fastapi import APIRouter, HTTPException, Depends, Form
from ..database import get_db
from ..schemas.project_content_schemas import ProjectContentOutput, ProjectContentInput
from sqlalchemy.orm import Session
from typing import List

from ..crud.crud_project_content import (
    create_project_content,
    delete_project_content,
    get_project_content_by_project_id,
    get_project_content,
    update_project_content,
)


router = APIRouter(
    prefix="/projects-contents",
    tags=["projects-contents"],
)


@router.post("", response_model=ProjectContentOutput)
async def make_project_content(
    data: ProjectContentInput, db: Session = Depends(get_db)
):
    project_content = create_project_content(data=data, db=db)
    return project_content


@router.get("", response_model=List[ProjectContentOutput])
async def get_projects(project_id: int, db: Session = Depends(get_db)):
    """다수의 project 조회

    Args:
        user_id (int): user의 pk
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: _description_

    Returns:
        List: List[ProjectContentOutput]
    """
    project_contents = get_project_content_by_project_id(project_id=project_id, db=db)
    if project_contents is None:
        raise HTTPException(status_code=404, detail="ProjectContent not found")
    return project_contents


@router.get("/{project_content_id}", response_model=ProjectContentOutput)
async def get_one_project_content(
    project_content_id: int, db: Session = Depends(get_db)
):
    """project_id로 단일 project 조회

    Args:
        project_content_id (int): project pk
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: _description_

    Returns:
        dict: ProjectContentOutput
    """
    project_content = get_project_content(project_content_id=project_content_id, db=db)
    if project_content is None:
        raise HTTPException(status_code=404, detail="ProjectContent not found")
    return project_content


@router.put("/{project_content_id}", response_model=ProjectContentOutput)
async def change_project_content(
    project_content_id: int, data: ProjectContentInput, db: Session = Depends(get_db)
):
    """project 수정

    Args:
        project_content_id (int): project pk
        data (ProjectContentInput): ProjectContentInput
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: _description_

    Returns:
        _type_: ProjectContentOutput
    """
    project = update_project_content(
        project_content_id=project_content_id, data=data, db=db
    )
    if not project:
        raise HTTPException(status_code=400, detail="Update failed")
    return project


@router.delete("/{project_content_id}", response_model=dict)
async def erase_project_content(project_content_id: int, db: Session = Depends(get_db)):
    """project content 삭제

    Args:
        project_content_id (int): project pk
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: _description_

    Returns:
        _type_: dict 성공시 {"success" : True}
    """
    success = delete_project_content(project_content_id=project_content_id, db=db)
    if not success:
        raise HTTPException(status_code=400, detail="Delete failed")
    return {"success": True}
