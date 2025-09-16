import datetime

from pydantic import BaseModel


class HistoryResponse(BaseModel):
    id: int
    rev_description: str
    note_id: int
    note_title: str
    note_content: str
    created_at: datetime.datetime

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "rev_description": "Created note",
                    "note_id": 2,
                    "note_title": "Implement project",
                    "note_content": "Start implementing the final project of the internship.",
                    "created_at": "2025-09-01T07:41:59.496609",
                }
            ]
        }
    }
