# 2024/2/6
# zhangzhong


from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.common import model
from app.database import DatabaseService, schema


def get_db() -> DatabaseService:
    return DatabaseService()


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")


def parse_token(token: str) -> model.TokenData:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    uid: str | None = payload.get("sub")
    if uid is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return model.TokenData(uid=int(uid))


async def get_token_data(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> model.TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        uid: str | None = payload.get("sub")
        if uid is None:
            raise credentials_exception
        token_data = model.TokenData(uid=int(uid))
    except JWTError:
        raise credentials_exception
    return token_data


def get_user(
    token_data: Annotated[model.TokenData, Depends(get_token_data)],
    db: Annotated[DatabaseService, Depends(get_db)],
) -> schema.User:
    user = db.get_user(uid=token_data.uid)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_admin(
    user: Annotated[schema.User, Depends(get_user)],
) -> schema.User:
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Permission denied",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
