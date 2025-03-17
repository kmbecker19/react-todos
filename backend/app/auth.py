from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, SQLModel, select

from .models import User, UserPublic
from .api import SessionDep

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')
TokenDep = Annotated[str, Depends(oauth2_scheme)]

def get_current_user(token: TokenDep, session: SessionDep) -> User:
    user = session.exec(select(User).where(User.username == token)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
    return user

UserDep = Annotated[User, Depends(get_current_user)]