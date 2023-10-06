from datetime import datetime

from .database import Base
from .enums.state import TodoState
from sqlalchemy import Column, Integer, TEXT, DateTime, ForeignKey, Enum as EnumColumn
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    email = Column(TEXT, nullable=False, unique=True)
    password = Column(TEXT, nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)

    projects = relationship("Project", back_populates="user")


class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    title = Column(TEXT)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(
        DateTime, default=datetime.now(), nullable=False, onupdate=func.now()
    )
    start_at = Column(DateTime)
    end_at = Column(DateTime)
    tech = Column(TEXT)
    categories = Column(TEXT)
    description = Column(TEXT)

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="projects")

    project_contents = relationship("ProjectContent", back_populates="project")
    project_todos = relationship("ProjectTodo", back_populates="project")
    project_design_setting = relationship(
        "ProjectDesignSetting", back_populates="project"
    )


class ProjectContent(Base):
    __tablename__ = "project_content"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    order = Column(Integer)
    title = Column(TEXT)
    imageUrl = Column(TEXT)
    contents = Column(TEXT)

    project_id = Column(Integer, ForeignKey("project.id"))
    project = relationship("Project", back_populates="project_contents")


class ProjectDesignSetting(Base):
    __tablename__ = "project_design_setting"

    id = Column(Integer, primary_key=True, index=True, unique=True)

    project_id = Column(Integer, ForeignKey("project.id"))
    project = relationship("Project", back_populates="project_design_setting")


class ProjectTodo(Base):
    __tablename__ = "project_todo"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    state = Column(EnumColumn(TodoState))
    priority = Column(Integer)

    project_id = Column(Integer, ForeignKey("project.id"))
    project = relationship("Project", back_populates="project_todos")
