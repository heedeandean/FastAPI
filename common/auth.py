from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from jose import JWTError, jwt
from enum import StrEnum
from dataclasses import dataclass
from config import get_settings

settings = get_settings()

SECRET_KEY = settings.jwt_secret
ALGORITHM = 'HS256'

class Role(StrEnum):
    ADMIN = 'ADMIN'
    USER = 'USER'

@dataclass
class CurrentUser:
    id: str
    role: Role

    def __str__(self):
        return f'{self.id}({self.role})'


def create_access_token(payload: dict, 
                        role: Role, 
                        expires_delta: timedelta = timedelta(hours=6)):
    expire = datetime.utcnow() + expires_delta
    payload.update({'role': role, 'exp': expire})
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def decode_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)   

oaut2_scheme = OAuth2PasswordBearer(tokenUrl='/users/login')
def get_current_user(token: Annotated[str, Depends(oaut2_scheme)]):
    payload = decode_access_token(token)

    user_id = payload.get('user_id')
    role = payload.get('role')
    if not user_id or not role or role != Role.USER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return CurrentUser(user_id, Role(role))

def get_admin_user(token: Annotated[str, Depends(oaut2_scheme)]):
    payload = decode_access_token(token)

    role = payload.get('role')
    if not role or role != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return CurrentUser('ADMIN_USER_ID', role)