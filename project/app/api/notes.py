from typing import List

from app.api import crud
from app.models.pydantic import NotePayloadSchema, NoteResponseSchema
from app.models.tortoise import NoteSchema
from app.models.user import User, get_current_user
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/", response_model=NoteResponseSchema, status_code=201)
async def create_note(
    payload: NotePayloadSchema, current_user: User = Depends(get_current_user)
) -> NoteResponseSchema:
    note_id, note_title, note_content = await crud.post(payload, current_user.username)

    response_object = {
        "id": note_id,
        "title": note_title,
        "content": note_content,
    }
    return response_object


@router.get("/", response_model=List[NoteSchema])
async def read_all_notes(
    current_user: User = Depends(get_current_user),
) -> List[NoteSchema]:
    return await crud.get_all(current_user.username)
