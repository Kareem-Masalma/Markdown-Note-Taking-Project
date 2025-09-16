import datetime

from pydantic import BaseModel


class RenderResponse(BaseModel):
    note_id: int
    rendered_html: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "note_id": 2,
                    "rendered_text": "<h1>This is a title</h1>\n<p>This is a paragraph.</p>\n",
                }
            ]
        }
    }
