from pydantic import BaseModel, Field


class ChildNotes(BaseModel):
    """Schema of a child note for a parent folder"""

    id: int
    title: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "title": "Implement the project",
                }
            ]
        }
    }


class ParentOut(BaseModel):
    id: int
    name: str

    model_config = {"json_schema_extra": {"examples": [{"id": 1, "name": "Projects"}]}}


class FolderIn(BaseModel):
    name: str = Field(..., description="The name field for the folder.")
    parent: int = Field(default=0, description="The id of the parent folder.")

    model_config = {
        "json_schema_extra": {"examples": [{"name": "Projects", "parent": 0}]}
    }


class FolderOut(BaseModel):
    id: int
    name: str
    parent: ParentOut

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"id": 1, "name": "Projects", "parent": {"id": 0, "name": "root"}}
            ]
        }
    }
