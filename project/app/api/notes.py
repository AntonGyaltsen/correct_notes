from typing import List

from fastapi import APIRouter, HTTPException, Depends, Header, status
from passlib.context import CryptContext

from app.api import crud
from app.models.pydantic import NotePayloadSchema, NoteResponseSchema
from app.models.tortoise import NoteSchema

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {
    "user1": {
        "username": "user1",
        "hashed_password": pwd_context.hash("password1")
    },
    "user2": {
        "username": "user2",
        "hashed_password": pwd_context.hash("password2")
    }
}


class User:
    def __init__(self, username: str):
        self.username = username

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password,
                                  fake_users_db[self.username]["hashed_password"])


async def get_user(username: str):
    if username in fake_users_db:
        return User(username=username)
    return None


async def get_current_user(username: str = Header(...), password: str = Header(...)):
    user = await get_user(username)
    if not user or not user.verify_password(password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user


@router.post("/", response_model=NoteResponseSchema, status_code=201)
async def create_note(payload: NotePayloadSchema, current_user: User = Depends(
    get_current_user)) -> NoteResponseSchema:
    note_id = await crud.post(payload, current_user.username)

    response_object = {
        "id": note_id,
        "title": payload.title,
        "content": payload.content,
    }
    return response_object


@router.get("/", response_model=List[NoteSchema])
async def read_all_notes(current_user: User = Depends(
    get_current_user)) -> List[NoteSchema]:
    return await crud.get_all(current_user.username)
