from pydantic import BaseModel


class ParentOut(BaseModel):
    id: int
    name: str
