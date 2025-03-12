from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlmodel import create_engine, Session, SQLModel, select
from pathlib import Path
from typing import Annotated
from uuid import UUID, uuid4

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# SQL Server Routes
@app.get('/sql/todo', response_model=list[TodoPublic])
def read_sql_todos(session: SessionDep,
                   offset: int = 0,
                   limit: Annotated[int, Query(le=100)] = 100,
                   sort: Annotated[str, Query(pattern='^(default|date|priority)$')] = 'default'):
    query = select(Todo).offset(offset).limit(limit)
    if sort == 'priority':
        query = query.order_by(Todo.priority.desc())
    elif sort == 'date':
        query = query.order_by(Todo.due_date)
    todos = session.exec(query).all()
    return todos


@app.post('/sql/todo', response_model=TodoPublic)
def create_sql_todo(session: SessionDep, todo_create: TodoCreate):
    todo_db = Todo.model_validate(todo_create)
    session.add(todo_db)
    session.commit()
    session.refresh(todo_db)
    return todo_db


@app.put('/sql/todo/{id}', response_model=TodoPublic)
def update_sql_todo(id: UUID | str, todo_update: TodoUpdate, session: SessionDep):
    todo_db = session.get(Todo, id)
    if not todo_db:
        raise HTTPException(status_code=404, detail='Todo not found')
    todo_data = todo_update.model_dump(exclude_unset=True)
    todo_db.sqlmodel_update(todo_data)
    session.add(todo_db)
    session.commit()
    session.refresh(todo_db)
    return todo_db


@app.delete('/sql/todo/{id}')
def delete_sql_todo(id: UUID | str, session: SessionDep):
    todo = session.get(Todo, id)
    if not todo:
        raise HTTPException(status_code=404, detail='Todo not found')
    session.delete(todo)
    session.commit()
    return {'ok': True}
