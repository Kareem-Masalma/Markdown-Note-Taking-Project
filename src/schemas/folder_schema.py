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


class FolderIn(BaseModel):
    name: str = Field(..., description="The name field for the folder.")
    parent: int = Field(default=0, description="The id of the parent folder.")


class FolderOut(BaseModel):
    id: int
    name: str
    parent: ParentOut
