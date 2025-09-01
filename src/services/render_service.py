from fastapi import HTTPException

from src.common.utils.render_markdown import render_markdown_to_html
from src.models.note import Note
from src.repositories.note_repository import NoteRepository


class RenderService:
    def __init__(self, note_repository: NoteRepository):
        self.note_repository = note_repository

    async def render(self, note_id: int):
        try:
            note: Note = await self.note_repository.get_note_by_id(note_id)

            if not note:
                raise HTTPException(status_code=404, detail="Note not found")

            markdown_text = note.content
            html_text = render_markdown_to_html(markdown_text)
            return html_text
        except Exception as e:
            raise e
