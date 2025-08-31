from fastapi import FastAPI

from src.routers.user_router import router as user_router
from src.routers.note_router import router as note_router
from src.routers.render_router import router as render_router
from src.routers.folder_router import router as folder_router
from src.routers.tag_router import router as tag_router
from src.routers.summarizaton_router import router as summarization_router

tags_metadata = [
    {
        "name": "Users",
        "description": "Operations with users, registration and login.",
    },
    {
        "name": "Notes",
        "description": "Manage user's notes, CRUD operations, fix issues with notes, and go back to certain state of a note.",
    },
    {
        "name": "Folders",
        "description": "Manage folders and their subfolders and notes.",
    },
    {
        "name": "Tags",
        "description": "Manage tags, CRUD operations and their notes.",
    },
    {
        "name": "Render",
        "description": "Endpoint to fetch sanitized HTML derived from Markdown.",
    },
    {
        "name": "External",
        "description": "Endpoint to call api that summarizes a note or a folder.",
    },
]

app = FastAPI(
    title="Revisionary",
    description="Backend service that allows users to manage their notes.",
    version="1.0.0",
    contact={
        "name": "Kareem Masalma",
        "email": "kareem@example.com",
    },
    openapi_tags=tags_metadata,
)

app.include_router(user_router, prefix="/user", tags=["Users"])
app.include_router(note_router, prefix="/note", tags=["Notes"])
app.include_router(folder_router, prefix="/folder", tags=["Folders"])
app.include_router(tag_router, prefix="/tag", tags=["Tags"])
app.include_router(render_router, prefix="/render", tags=["Render"])
app.include_router(summarization_router, prefix="/summ", tags=["External"])


@app.get("/")
async def root():
    return {"Welcome": "The application is running"}
