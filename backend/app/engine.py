from sqlmodel import create_engine, Session
from pathlib import Path
from typing import Annotated
from fastapi import Depends

# Set up SQL Engine
db_path = Path().absolute() / 'backend' / 'todos.db'
sqlite_url = f'sqlite:///{db_path}'
connect_args = {'check_same_thread': False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
