from pydantic import BaseModel


class NotePayloadSchema(BaseModel):
    title: str
    content: str


class NoteResponseSchema(NotePayloadSchema):
    id: int
