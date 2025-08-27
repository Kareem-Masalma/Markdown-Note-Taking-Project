from typing import Optional

from pydantic import BaseModel, Field


class NoteIn(BaseModel):
    title: str = Field
    content: str = Field
    user: int = Field
