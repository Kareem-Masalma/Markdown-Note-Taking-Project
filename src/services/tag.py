from fastapi import HTTPException

from src.models.note import Note
from src.models.tag import Tag
from src.repositories.tag import TagRepository
from src.schemas.tag import TagRequest, TagResponse


class TagService:
    def __init__(self, tag_repository: TagRepository):
        self.tag_repository = tag_repository

    async def create_tag(self, tag: TagRequest):
        """
        This method to create a new tag that doesn't exist in the database.

        :param tag: The tag to add.
        :return: The successfully added tag.
        """
        exists = self.check_tag_existence(tag.name)
        if exists:
            raise HTTPException(status_code=409, detail="Folder already exists.")

        new_tag: Tag = Tag(name=tag.name)
        await self.tag_repository.create(new_tag)

        return {
            "details": "Folder is added successfully",
            "folder": {"id": new_tag.id, "title": new_tag.name},
        }

    async def get_all_tags(self):
        """
        This method to get all tags.

        :return: All tags in database.
        """
        tags: list[Tag] = await self.tag_repository.get_all()
        if not tags:
            raise HTTPException(status_code=404, detail="No tags found.")
        return tags

    async def get_tag_by_id(self, tag_id: int):
        """
        This method to get a tag by its id.

        :param tag_id: The id of the tag to get.
        :return: The tag.
        """

        tag: Tag = await self.tag_repository.get_by_id(tag_id)
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found.")
        return tag

    async def get_tag_by_name(self, tag_name: str):
        """
        This method to get a tag by its name.

        :param tag_name: The name of the tag to get.
        :return: The tag.
        """
        try:
            tag = await self.tag_repository.get_tag_by_name(tag_name)
            return tag
        except Exception as e:
            raise e

    async def rename_tag(self, tag_id: int, new_name: str):
        """
        This method to rename a certain tag by its id.

        :param tag_id: The tag to be renamed.
        :param new_name: The new name for the tag.
        :return: The new tag.
        """
        try:
            stored_tag = await self.tag_repository.get_by_id(tag_id)

            if not stored_tag:
                raise HTTPException(status_code=404, detail="Tag not found")

            await self.tag_repository.rename_tag(stored_tag, new_name)

            tag_out = TagResponse(id=stored_tag.id, name=stored_tag.name)
            return tag_out
        except Exception as e:
            raise e

    async def delete_tag(self, tag_id: int):
        """
        This method to delete a tag by its id.

        :param tag_id: The id of the tag to delete.
        :return: If the tag is deleted.
        """
        try:
            exists = self.get_tag_by_id(tag_id)

            if not exists:
                raise HTTPException(status_code=404, detail="Tag not found.")

            await self.tag_repository.delete(tag_id)
            return True
        except Exception as e:
            raise e

    async def get_tag_notes(self, tag_id: int):
        """
        This method to get the notes of a certain tag.

        :param tag_id: The id of the tag to get its notes.
        :return: The notes' of the tag.
        """
        try:
            exists = self.get_tag_by_id(tag_id)

            if not exists:
                raise HTTPException(status_code=404, detail="Tag not found.")

            notes: list[Note] = await self.tag_repository.get_tag_notes(tag_id)

            return notes
        except Exception as e:
            raise e

    async def check_tag_existence(self, tag_name: str) -> bool:
        """
        This method to check if a tag exists.

        :param tag_name: The name of the tag to check.
        :return: If the tag exists or not.
        """
        try:
            exist = await self.get_tag_by_name(tag_name)
            if exist:
                return True
            return False
        except Exception as e:
            raise e
