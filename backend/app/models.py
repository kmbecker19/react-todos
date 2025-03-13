from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from typing import Annotated
from fastapi import Query


# Force Dates to fit YYYY-MM-DD format
date_pattern = r'^[1-2]\d{3}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$'
DateStr = Annotated[str, Query(pattern=date_pattern)]


class TodoBase(SQLModel):
    item: str | None = Field(index=True, default=None, unique=True)
    due_date: DateStr | None = Field(index=True, default=None)
    priority: Annotated[int, Query(ge=1, le=3)] | None = Field(index=True, default=None)
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
    priority: Annotated[int, Query(ge=1, le=3)] | None = None
    completed: bool | None = None
