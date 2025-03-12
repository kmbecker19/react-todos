from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4

class TodoBase(SQLModel):
    item: str | None = Field(index=True, default=None)

class Todo(TodoBase, table=True):
    id: str = Field(primary_key=True, default_factory=lambda: str(uuid4()))

class TodoPublic(TodoBase):
    id: str
    item: str

class TodoCreate(TodoBase):
    item: str

class TodoUpdate(TodoBase):
    item: str | None = None