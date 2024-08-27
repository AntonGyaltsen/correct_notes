from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {
    "user1": {"username": "user1", "hashed_password": pwd_context.hash("password1")},
    "user2": {"username": "user2", "hashed_password": pwd_context.hash("password2")},
}


class User:
    def __init__(self, username: str):
        self.username = username

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(
            password, fake_users_db[self.username]["hashed_password"]
        )


async def get_user(username: str):
    if username in fake_users_db:
        return User(username=username)
    return None


security = HTTPBasic()


async def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = await get_user(credentials.username)
    if not user or not user.verify_password(credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user
