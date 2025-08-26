"""
This module is used to verify the inputs and outputs of the endpoints.
"""

from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserIn(BaseModel):
    """User base schema"""

    username: str
    email: EmailStr | None = Field(
        default=None, description="The user email, it should be in email format"
    )
    password: str = Field(
        Optional,
        min_length=8,
        max_length=32,
        description="The user password, it should be at least 8 characters long",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "Kareem",
                    "email": "Kareem@example.com",
                    "password": "security",
                }
            ]
        }
    }


class UserOut(BaseModel):
    """User response schema"""

    id: int
    username: str
    email: EmailStr

    model_config = {
        "json_schema_extra": {
            "examples": [{"id": 1, "username": "Kareem", "email": "Kareem@example.com"}]
        }
    }
