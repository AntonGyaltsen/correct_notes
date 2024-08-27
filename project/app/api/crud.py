from typing import List, Tuple, Any

from app.api.util import check_spelling
from app.models.pydantic import NotePayloadSchema
from app.models.tortoise import Note, NoteSchema


async def post(payload: NotePayloadSchema, user) -> tuple[Any, str, str]:
    corrected_title = await check_spelling(payload.title)
    corrected_content = await check_spelling(payload.content)
    note = Note(
        title=corrected_title,
        content=corrected_content,
        user=user,
    )
    await note.save()
    return note.id, corrected_title, corrected_content


async def get_all(user) -> List:
    notes = await NoteSchema.from_queryset(Note.filter(user=user).all())
    return notes
