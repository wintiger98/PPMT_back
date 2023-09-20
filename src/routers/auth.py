from fastapi import APIRouter, HTTPException, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

from ..crud.crud_auth import (
    create_user,
    delete_user,
    get_access_token,
    get_current_user_email,
    get_user_by_email,
    get_user_by_id_password,
    get_user_by_user_id,
    update_user,
)
from ..schemas.auth_schemas import UserBase, UserOutput, Token, TokenData

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = get_user_by_id_password(
        email=form_data.username, password=form_data.password, db=db
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = get_access_token(data={"email": user.email})
    return access_token


@router.post("/signup", response_model=UserOutput)
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
    user = get_user_by_id_password(
        email=user_data.email, password=user_data.password, db=db
    )
    if user:
        raise HTTPException(status_code=400)
    user = create_user(email=user_data.email, password=user_data.password, db=db)
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
    user = get_user_by_id_password(
        email=user_data.email, password=user_data.password, db=db
    )
    if not user:
        raise HTTPException(status_code=400)
    return user


@router.get("/me", response_model=UserOutput)
async def read_users_me(
    email: str = Depends(get_current_user_email), db: Session = Depends(get_db)
):
    user = get_user_by_email(email=email, db=db)
    if not user:
        raise HTTPException(status_code=400, detail="Not found User")
    return user


@router.put("/users", response_model=dict)
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


@router.delete("/users/{user_id}", response_model=dict)
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
