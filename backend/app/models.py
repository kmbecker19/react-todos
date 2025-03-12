from sqlmodel import SQLModel, Field

class TodoBase(SQLModel):
    item: str | None = Field(index=True, default=None)

class Todo(TodoBase, table=True):
    id: int | None = Field(primary_key=True)

class TodoPublic(TodoBase):
    id: int

class TodoCreate(TodoBase):
    item: str

class TodoUpdate(TodoBase):
    item: str | None = None