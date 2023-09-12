from fastapi import APIRouter, HTTPException, Depends, Form
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

from ..crud.crud_user import (
    create_user,
    delete_user,
    get_user_by_id_password,
    get_user_by_user_id,
    update_user,
)
from ..schemas.user_schemas import UserBase, UserOutput


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("", response_model=UserOutput)
async def sign_up(user_data: UserBase, db: Session = Depends(get_db)):
    """회원가입



    Parameters:
    ===========

    Args:
        user_data (UserBase): UserBase
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Returns:
    ========

        _type_: UserOutput
    """
    print(user_data.model_dump())
    user = create_user(
        user_name=user_data.user_name, password=user_data.password, db=db
    )
    return user


@router.post("/login", response_model=UserOutput)
async def login(user_data: UserBase, db: Session = Depends(get_db)):
    """로그인



    Parameters:
    ===========

    Args:
        user_data (UserBase): UserBase
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Returns:
    ========

        _type_: UserOutput
    """
    user = get_user_by_id_password(id=user_data.id, password=user_data.password, db=db)
    return user


@router.get("/{user_id}", response_model=UserOutput)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """## Args

    | Parameter | Type | Description |
    | --------- | ---- | ----------- |
    | user_id | int |  |


    ## Returns

    | Type | Description |
    | ---- | ----------- |
    | UserOutput |  |
    """
    user = get_user_by_user_id(user_id=user_id, db=db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=dict)
async def change_user(user_id: int, password: str, db: Session = Depends(get_db)):
    """## change user info

    | Parameter | Type | Description |
    | --------- | ---- | ----------- |
    | user_id | int |  |
    | password | str |  |


    ## Returns

    | Type | Description |
    | ---- | ----------- |
    | dict | {"success":true} |
    """
    success = update_user(user_id=user_id, password=password, db=db)
    if not success:
        raise HTTPException(status_code=400, detail="Update failed")
    return {"success": True}


@router.delete("/{user_id}", response_model=dict)
async def erase_user(user_id: int, db: Session = Depends(get_db)):
    """## delete user info

    | Parameter | Type | Description |
    | --------- | ---- | ----------- |
    | user_id | int |  |


    ## Returns

    | Type | Description |
    | ---- | ----------- |
    | dict | {"success":true} |
    """
    success = delete_user(user_id=user_id, db=db)
    if not success:
        raise HTTPException(status_code=400, detail="Delete failed")
    return {"success": True}
