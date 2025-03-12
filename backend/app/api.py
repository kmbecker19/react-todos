from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlmodel import create_engine, Session, SQLModel, select
from pathlib import Path
from typing import Annotated

from .models import Todo, TodoPublic, TodoCreate, TodoUpdate


# Set up SQL Engine
db_path = Path().absolute() / 'todos.db'
sqlite_url = f'sqlite:///{db_path}'
connect_args = {'check_same_thread': False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(lifespan=lifespan)


def get_session():
    with Session(engine) as session:
        yield session


# Session Dependency
SessionDep = Annotated[Session, Depends(get_session)]

origins = [
    "http://localhost:5173",
    "localhost:5173"
]

todos = [
    {"id": 1, "item": "Buy groceries"},
    {"id": 2, "item": "Clean the house"},
    {"id": 3, "item": "Complete project"}
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {'"message": "Welcome to your todo list."'}


# SQL Server Routes
@app.get('/sql/todo', response_model=list[TodoPublic])
def read_sql_todos(session: SessionDep):
    todos = session.exec(select(Todo)).all()
    if not todos:
        raise HTTPException(status_code=404, message='Todos not found')
    return todos


@app.post('/sql/todo', response_model=TodoPublic)
def create_sql_todo(session: SessionDep, todo_create: TodoCreate):
    todo_db = Todo.model_validate(todo_create)
    session.add(todo_db)
    session.commit()
    session.refresh(todo_db)
    return todo_db


@app.put('/sql/todo/{id}', response_model=TodoPublic)
def update_sql_todo(id: int, todo_update: TodoUpdate, session: SessionDep):
    todo_db = session.get(Todo, id)
    if not todo_db:
        raise HTTPException(status_code=404, message='Todo not found')
    todo_data = todo_update.model_dump(exclude_unset=True)
    todo_db.sqlmodel_update(todo_data)
    session.add(todo_db)
    session.commit()
    session.refresh(todo_db)
    return todo_db


# Local Dict routes
@app.get('/todo', tags=['todos'])
async def read_todos() -> dict:
    return {"data": todos}


@app.post('/todo', tags=['todos'])
async def create_todo(todo: dict) -> dict:
    todos.append(todo)
    return {'data': todo}


@app.put("/todo/{id}", tags=["todos"])
async def update_todo(id: int, body: dict) -> dict:
    for todo in todos:
        if int(todo["id"]) == id:
            todo["item"] = body["item"]
            return {
                "data": f"Todo with id {id} has been updated."
            }

    return {
        "data": f"Todo with id {id} not found."
    }


@app.delete("/todo/{id}", tags=["todos"])
async def delete_todo(id: int) -> dict:
    for todo in todos:
        if int(todo["id"]) == id:
            todos.remove(todo)
            return {
                "data": f"Todo with id {id} has been removed."
            }

    return {
        "data": f"Todo with id {id} not found."
    }
