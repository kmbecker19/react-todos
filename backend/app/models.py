from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from typing import Annotated, List
from fastapi import Query

# Usernames should be alphanumeric with underscores or dashes
username_pattern = r'^[a-zA-Z0-9_\-]+$'
# Passwords should be 3+ alphanumeric characters
password_pattern = r'^[a-zA-Z0-9_\-]{3,}$'

Username = Annotated[str, Query(pattern=username_pattern)]
Password = Annotated[str, Query(pattern=password_pattern)]

# User Models
class UserBase(SQLModel):
    username: Username = Field(index=True, unique=True)


class User(UserBase, table=True):
    id: str = Field(primary_key=True, default_factory=lambda: str(uuid4()))
    hashed_password: str = Field()

    todos: List['Todo'] = Relationship(back_populates='user')


class UserPublic(UserBase):
    id: str


class UserCreate(UserBase):
    password: Password


class UserUpdate(UserBase):
    username: Username | None = None
    password: Password | None = None


# Force Dates to fit YYYY-MM-DD format
date_pattern = r'^[1-2]\d{3}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$'
DateStr = Annotated[str, Query(pattern=date_pattern)]


# Todo Models
class TodoBase(SQLModel):
    item: str | None = Field(index=True, default=None, unique=True)
    due_date: DateStr | None = Field(index=True, default=None)
    priority: Annotated[int | None, Query(ge=1, le=3)] = Field(
        index=True, default=None)
    completed: bool = Field(index=True, default=False)


class Todo(TodoBase, table=True):
    id: str = Field(primary_key=True, default_factory=lambda: str(uuid4()))

    user_id: str | None = Field(default=None, foreign_key='user.id')
    user: User | None = Relationship(back_populates='todos')


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
