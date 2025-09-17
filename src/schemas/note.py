from typing import Optional, List

from pydantic import BaseModel, Field

from src.schemas.folder import ParentResponse
from src.schemas.tag import TagResponse


class NoteRequest(BaseModel):
    """Schema for creating a note"""

    title: str = Field(..., description="The title of the note")
    content: str = Field("", description="The content of the note")
    username: str = Field(..., description="The username who owns the note")
    tags: Optional[List[int]] = Field(
        default=[0], description="List of tag ids attached to the note"
    )
    parent_id: Optional[int] = Field(default=0)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Implement the project",
                    "content": "Finish the implementation of the final project for the internship",
                    "username": "kareem",
                    "tag_ids": [1, 2],
                }
            ]
        }
    }


class NoteResponse(BaseModel):
    """Schema for returning a note"""

    id: int
    title: str
    content: str
    username: str
    parent: ParentResponse
    tags: list[TagResponse]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "title": "Implement the project",
                    "content": "Finish the implementation of the final project for the internship",
                    "username": "kareem",
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
