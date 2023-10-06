from ..config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from ..models import User
from ..schemas.auth_schemas import TokenData

from fastapi import HTTPException
from datetime import timedelta, datetime
from sqlalchemy import select, delete, update, and_
from sqlalchemy.orm import Session
from jose import JWTError, jwt


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """## access token 만드는 함수

    | Parameter | Type | Description |
    | --------- | ---- | ----------- |
    | data | dict |  |
    | expires_delta | dict |  |


    ## Returns

    | Type | Description |
    | ---- | ----------- |
    | _type_ |  |
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    # 테스트를 위한 만료 기한 연장
    expire = datetime.utcnow() + timedelta(days=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_access_token(data: TokenData):
    """## 토큰 생성을 위한 함수

    | Parameter | Type | Description |
    | --------- | ---- | ----------- |
    | data | TokenData |  |


    ## Returns

    | Type | Description |
    | ---- | ----------- |
    | dict | access_token(str), token_type(str) |
    """
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": data["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user_email(token: str):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception
    return email


def get_user_by_user_id(user_id: int, db: Session):
    stmt = select(User).where(User.id == user_id)
    result = db.execute(stmt)
    user = result.scalar()
    return user


def get_user_by_email(email: str, db: Session):
    stmt = select(User).where(User.email == email)
    result = db.execute(stmt)
    user = result.scalar()
    return user


def get_user_by_id_password(email: str, password: str, db: Session):
    stmt = select(User).where(and_(User.email == email, User.password == password))
    result = db.execute(stmt)
    user = result.scalar()
    return user


def create_user(email: str, password: str, db: Session):
    user = User(email=email, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(user_id: int, password: str, db: Session):
    stmt = update(User).where(User.id == user_id).values(password=password)
    result = db.execute(stmt)
    db.commit()
    updated_rows = result.rowcount  # 업데이트된 row의 개수
    return updated_rows


def delete_user(user_id: int, db: Session):
    stmt = delete(User).where(User.id == user_id)
    db.execute(stmt)
    db.commit()
    return None
