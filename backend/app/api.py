from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlmodel import create_engine, Session, SQLModel, select
from pathlib import Path
from typing import Annotated
from uuid import UUID, uuid4

from .models import Todo, TodoPublic, TodoCreate, TodoUpdate, User, UserPublic, UserCreate
from .auth import get_password_hash, verify_password, authenticate_user
from .engine import engine, SessionDep

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)

app = FastAPI(lifespan=lifespan)


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
                   sort: Annotated[str, Query(pattern='^(default|date|priority)$')] = 'default',
                   filter: Annotated[str | None, Query(pattern='^(in)?complete$')] = None):
    query = select(Todo).offset(offset).limit(limit)
    if filter == 'complete':
        query = query.filter(Todo.completed == True)
    elif filter == 'incomplete':
        query = query.filter(Todo.completed == False)
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


# User Routes
@app.get('/auth/users', tags=['auth'], response_model=list[UserPublic])
def read_users(session: SessionDep):
    users = session.exec(select(User)).all()
    return users


@app.post('/auth/users', tags=['auth'], response_model=UserPublic)
def create_user(session: SessionDep, user_create: UserCreate):
    hashed_password = get_password_hash(user_create.password)
    extra_data = {'hashed_password': hashed_password}
    user_db = User.model_validate(user_create, update=extra_data)
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db