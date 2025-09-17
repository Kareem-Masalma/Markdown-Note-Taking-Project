from fastapi import HTTPException, Response

from src.common.utils.generate_etag import generate_etag
from src.common.utils.render_markdown import render_markdown_to_html
from src.models.note import Note
from src.repositories.note import NoteRepository
from src.schemas.render import RenderResponse


class RenderService:
    def __init__(self, note_repository: NoteRepository):
        self.note_repository = note_repository

    async def render(self, if_none_match, response: Response, note_id: int):
        """
        This method to render a Markdown text to a sanitized HTML code.

        :param if_none_match: Etag to check of the note is modified.
        :param response: The response to get the etag.
        :param note_id: The id of the note to render.
        :return: The rendered text.
        """
        try:
            note: Note = await self.note_repository.get_by_id(note_id)

            if not note:
                raise HTTPException(status_code=404, detail="Note not found")

            etag = generate_etag(note.content)
            response.headers["ETag"] = etag

            if etag == if_none_match:
                raise HTTPException(status_code=304, detail="Not modified")

            markdown_text = note.content
            rendered_html = render_markdown_to_html(markdown_text)
            return RenderResponse(note_id=note_id, rendered_html=rendered_html)
        except Exception as e:
            raise e
