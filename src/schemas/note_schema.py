from typing import Optional, List

from pydantic import BaseModel, Field


class NoteIn(BaseModel):
    """Schema for creating a note"""

    title: str = Field(..., description="The title of the note")
    content: str = Field("", description="The content of the note")
    user_id: int = Field(..., description="The ID of the user who owns the note")
    tag_ids: Optional[List[int]] = Field(
        default=[], description="List of tag IDs attached to the note"
    )
    parent_id: Optional[int] = Field(default="root")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Implement the project",
                    "content": "Finish the implementation of the final project for the internship",
                    "user_id": 1,
                    "tag_ids": [1, 2],
                }
            ]
        }
    }


class NoteOut(BaseModel):
    """Schema for returning a note"""

    id: int
    title: str
    content: str
    username: str
    tags: List[str]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "title": "Implement the project",
                    "content": "Finish the implementation of the final project for the internship",
                    "username": "kareem",
                    "tags": ["Project", "Implementation"],
                }
            ]
        }
    }


class NoteUpdate(BaseModel):
    """Schema for updating a note"""

    title: Optional[str] = Field(None, description="The new title of the note")
    content: Optional[str] = Field(None, description="The new content of the note")
    tag_ids: Optional[List[int]] = Field(
        None, description="Updated list of tag IDs attached to the note"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Updated project title",
                    "content": "Refactor the project to improve maintainability",
                    "tag_ids": [2, 3],
                }
            ]
        }
    }
