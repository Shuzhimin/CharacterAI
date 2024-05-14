# 2024/4/25
# zhangzhong

from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

# JWT
# base64 encoding, not enctypted
# but it is signed by the server, But it's signed. So, when you receive a token that you emitted, you can verify that you actually emitted it.
# https://github.com/mpdavis/python-jose
# https://jwt.io/

# password hasing and salt
# https://passlib.readthedocs.io/en/stable/

# to get a string like this run:
# openssl rand -hex 32
# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# # Create a variable ALGORITHM with the algorithm used to sign the JWT token and set it to "HS256"
# ALGORITHM = "HS256"
# # Create a variable for the expiration of the token.
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# # 这个东西需要单独拿出来 她可以被很多模块使用
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# https://datatracker.ietf.org/doc/html/rfc7519#section-4.1
# Create a utility function to generate a new access token.
# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.now(timezone.utc) + expires_delta
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# Create a variable ALGORITHM with the algorithm used to sign the JWT token and set it to "HS256"
ALGORITHM = "HS256"
# Create a variable for the expiration of the token.
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 这个东西需要单独拿出来 她可以被很多模块使用
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def encrypt_password(password: str) -> str:
    return pwd_context.hash(password)
