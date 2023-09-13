from ..models import User
from sqlalchemy import select, delete, update, and_
from sqlalchemy.orm import Session


def get_user_by_user_id(user_id: int, db: Session):
    stmt = select(User).where(User.id == user_id)
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
