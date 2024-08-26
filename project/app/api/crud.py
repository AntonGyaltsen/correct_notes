from typing import List

from app.models.pydantic import NotePayloadSchema
from app.models.tortoise import Note, NoteSchema


async def post(payload: NotePayloadSchema, user) -> int:
    note = Note(
        title=payload.title,
        content=payload.content,
        user=user,
    )
    await note.save()
    return note.id


async def get_all(user) -> List:
    notes = await NoteSchema.from_queryset(Note.filter(user=user).all())
    return notes
