from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from typing import Annotated
from fastapi import Query


# Force Dates to fit YYYY-MM-DD format
date_pattern = r'^[1-2]\d{3}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$'
DateStr = Annotated[str, Query(pattern=date_pattern)]

# Todo Models
class TodoBase(SQLModel):
    item: str | None = Field(index=True, default=None, unique=True)
    due_date: DateStr | None = Field(index=True, default=None)
    priority: Annotated[int | None, Query(ge=1, le=3)] = Field(index=True, default=None)
    completed: bool = Field(index=True, default=False)


class Todo(TodoBase, table=True):
    id: str = Field(primary_key=True, default_factory=lambda: str(uuid4()))


class TodoPublic(TodoBase):
    id: str
    item: str


class TodoCreate(TodoBase):
    item: str


class TodoUpdate(TodoBase):
    item: str | None = None
    due_date: DateStr | None = None
    priority: Annotated[int | None, Query(ge=1, le=3)] = None
    completed: bool | None = None


# User Models
class UserBase(SQLModel):
    username: str = Field(index=True)


class User(UserBase, table=True):
    id: str = Field(primary_key=True, default_factory=lambda: str(uuid4()))
    password: str


class UserPublic(UserBase):
    id: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    username: str | None = None
    password: str | None = None