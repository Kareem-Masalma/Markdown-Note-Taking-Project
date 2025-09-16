"""
This module is the methods used to handle notes endpoint operations, get note by id, get all notes,
delete note, update note, add new note.
"""

from fastapi import HTTPException

from src.models.note import Note
from src.repositories.note import NoteRepository
from src.schemas.folder import ParentResponse
from src.schemas.note import NoteUpdate, NoteRequest, NoteResponse
from src.schemas.tag import TagResponse

# from src.services.redis import RedisCache
from src.services.history import HistoryService


# redis_service = RedisCache()


# async def check_cache(key: str):
#     res = await redis_service.get(key)
#     return res
#
#
# async def write_on_cache(key: str, value: str, expire: int = 300):
#     await redis_service.set(key, value, expire)


class NoteService:

    def __init__(
        self, note_repository: NoteRepository, history_service: HistoryService
    ) -> None:
        self.note_repository = note_repository
        self.history_service = history_service

    async def get_all_notes(self) -> list[NoteResponse] | None:
        """
        This method is used to get all available notes inside the database with deleted field set to 0,
        it returns all notes if found, else it raises 404 HTTPException.

        :return: The returned value is a list of notes if found.
        """
        try:

            # res = await check_cache(ALL_NOTES_REDIS_KEY)
            #
            # if res:
            #     notes = json.loads(res)
            #     notes_out = [NoteOut(**note) for note in notes]
            #     return notes_out

            notes: list[Note] | None = await self.note_repository.get_all()
            if not notes:
                raise HTTPException(status_code=404, detail="No notes are found")

            notes_out = [
                NoteResponse(
                    id=note.id,
                    title=note.title,
                    content=note.content,
                    username=note.user.username,
                    parent=ParentResponse(id=note.parent.id, name=note.parent.name),
                    tags=[TagResponse(id=tag.id, name=tag.name) for tag in note.tags],
                )
                for note in notes
            ]
            # await write_on_cache(
            #     ALL_NOTES_REDIS_KEY, json.dumps([note.dict() for note in notes_out])
            # )

            return notes_out
        except Exception as e:
            raise e

    async def get_note_by_note_id(self, note_id: int) -> NoteResponse | None:
        """
        This method is used to get an available note with deleted field set to 0 by their note_id,
        it returns the note if found, else it raises a 404 HTTPException.
        :param note_id: The id of the note to be found.
        :return: The note's data.
        """
        try:

            # res = await check_cache(NOTE_ID_REDIS_KEY + f"/{note_id}")
            #
            # if res:
            #     res_note = json.loads(res)
            #     notes_out = NoteOut(**res_note)
            #     return notes_out

            note: Note | None = await self.note_repository.get_by_id(note_id)
            if not note:
                raise HTTPException(status_code=404, detail=f"Note {note_id} not found")

            note_out = NoteResponse(
                id=note.id,
                title=note.title,
                content=note.content,
                username=note.user.username,
                parent=ParentResponse(id=note.parent.id, name=note.parent.name),
                tags=[TagResponse(id=tag.id, name=tag.name) for tag in note.tags],
            )

            # await write_on_cache(
            #     NOTE_ID_REDIS_KEY + f"/{note_id}", json.dumps(note_out.dict())
            # )

            return note_out
        except Exception as e:
            raise e

    async def update_note(self, note_id: int, note: NoteUpdate) -> NoteResponse:
        """
        This method is used to update an available note from database with deleted field set to 0,
        exclude_unset is set to be True, which removes the empty fields that aren't meant to be updated.

        :param note_id: The id of the note to be updated.
        :param note: New note's data to update.
        :return: The update note, if not found it raised 404 HTTPException.
        """
        try:
            stored_note = await self.note_repository.get_by_id(note_id)

            if not stored_note:
                raise HTTPException(status_code=404, detail=f"Note {note_id} not found")

            await self.note_repository.update_note(stored_note, note)

            await self.history_service.create_new_history_version(
                stored_note, f"Note updated"
            )

            note_response = NoteResponse(
                id=note.id,
                title=note.title,
                content=note.content,
                username=note.user.username,
                parent=ParentResponse(id=note.parent.id, name=note.parent.name),
                tags=[TagResponse(id=tag.id, name=tag.name) for tag in note.tags],
            )
            return note_response
        except Exception as e:
            raise e

    async def delete_note(self, note_id: int) -> Note | None:
        """
        This method to delete an available note from database with deleted fild set to 1, this method softly deletes the
        user, which means the note is not removed from the database, but the deleted field will be set to 1.

        :param note_id: The id of the note to be deleted.
        :return: True on Success, else it raised 404 HTTPException.
        """
        try:
            exists = await self.note_repository.get_by_id(note_id)

            if not exists:
                raise HTTPException(status_code=404, detail="Note not found.")

            await self.note_repository.delete(note_id)

            await self.history_service.create_new_history_version(
                exists, f"Note deleted"
            )
            return exists
        except Exception as e:
            raise e

    async def add_new_note(self, note: NoteRequest) -> Note | None:
        """
        This method to add new note to the database.

        :param note: The new note information.
        :return: The new note created.
        """
        try:
            new_note = Note(
                title=note.title,
                content=note.content,
                user_id=note.user_id,
                parent_id=note.parent_id,
            )

            await self.note_repository.create(new_note)

            tags = note.tag_ids
            if tags:
                for tag in tags:
                    await self.note_repository.add_tag_note(new_note.id, tag)

            await self.history_service.create_new_history_version(
                new_note, f"Note created: {note.id}, {note.title}"
            )
            return new_note
        except Exception as e:
            raise e

    async def get_user_notes(self, user_id: int) -> list[NoteResponse]:
        """
        This method to get all notes that belongs to certain user by their id.

        :param user_id: The id of the user to get their notes.
        :return: User notes.
        """
        try:
            notes: list[Note] | None = await self.note_repository.get_user_notes(
                user_id
            )
            if not notes:
                raise HTTPException(status_code=404, detail="No notes are found")

            return [
                NoteResponse(
                    id=note.id,
                    title=note.title,
                    content=note.content,
                    username=note.user.username,
                    parent=ParentResponse(id=note.parent.id, name=note.parent.name),
                    tags=[TagResponse(id=tag.id, name=tag.name) for tag in note.tags],
                )
                for note in notes
            ]
        except Exception as e:
            raise e
