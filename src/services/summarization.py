from fastapi import HTTPException

from src.models.note import Note
from src.repositories.note import NoteRepository
from src.common.utils.gemini_api import send_to_gemini

# from src.services.redis import RedisCache

# redis_service = RedisCache()


# async def check_cache(key: str):
#     res = await redis_service.get(key)
#     return res
#
#
# async def write_on_cache(key: str, value: str, expire: int = 3600):
#     await redis_service.set(key, value, expire)


class SummarizeNotes:
    """This module to summarize notes"""

    def __init__(self, note_repository: NoteRepository):
        self.note_repository = note_repository

    async def summarize(self, note_id: int):
        """
        This method to summarize note by its id, it first checks the cache, if not found it calls the API.

        :param note_id: The id of the note to be checked.
        :return: The summary.
        """
        try:
            note: Note = await self.note_repository.get_by_id(note_id)

            if not note:
                raise HTTPException(status_code=404, detail="Note not found")

            # res = await check_cache(SUMMARY_KEY)
            # if res:
            #     return {"note": {"id": note.id, "title": note.title}, "summary": res}

            response = await send_to_gemini(
                f"Summarize this note in a few sentences:\n\n{note.content}"
            )
            summarization = response.candidates[0].content.parts[0].text

            # await write_on_cache(SUMMARY_KEY, summarization)

            return {
                "note": {"id": note.id, "title": note.title},
                "summary": summarization,
            }
        except Exception as e:
            raise e
