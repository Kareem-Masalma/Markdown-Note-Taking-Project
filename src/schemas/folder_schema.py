from pydantic import BaseModel, Field

from src.schemas.note_schema import ChildNotes


class ParentOut(BaseModel):
    id: int
    name: str


class FolderIn(BaseModel):
    name: str = Field(..., description="The name field for the folder.")
    parent: int = Field(default=0, description="The id of the parent folder.")


class FolderOut(BaseModel):
    id: int
    name: str
    parent: ParentOut
    notes: list[ChildNotes]
