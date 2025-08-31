from abc import ABC, abstractmethod

from src.schemas.tag_schema import TagIn


class ITagRepository(ABC):

    @abstractmethod
    async def create_tag(self, tag: TagIn):
        pass

    @abstractmethod
    async def get_all_tags(self):
        pass

    @abstractmethod
    async def get_tag_by_id(self, tag_id: int):
        pass

    @abstractmethod
    async def rename_tag(self, tag_id: int, new_name: str):
        pass

    @abstractmethod
    async def delete_tag(self, tag_id: int):
        pass

    @abstractmethod
    async def get_tag_notes(self, tag_id: int):
        pass
