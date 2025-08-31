from pydantic import BaseModel, Field


class TagOut(BaseModel):
    """The response schema of tags."""

    id: int
    name: str

    model_config = {
        "json_schema_extra": {"examples": [{"id": 0, "name": "Internship"}]}
    }


class TagIn(BaseModel):
    """The input schema of tags."""

    name: str = Field(..., title="Name of the Tag", description="The name of the tag.")

    model_config = {"json_schema_extra": {"examples": [{"name": "Internship"}]}}
