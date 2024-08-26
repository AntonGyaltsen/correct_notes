from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Note(models.Model):
    title = fields.CharField(max_length=255)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    user = fields.CharField(max_length=50)

    def __str__(self):
        return self.title


NoteSchema = pydantic_model_creator(Note)
