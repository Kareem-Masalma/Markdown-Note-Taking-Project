from fastapi import HTTPException

from src.common.utils.grammar_checker import GrammarChecker
from src.models.history import History
from src.repositories.history_repository import HistoryRepository


class LanguageToolService:

    def __init__(self, history_repository: HistoryRepository):
        self.history_repository = history_repository

    async def check_grammar(self, version_id: int):
        version: History = await self.history_repository.get_version_by_id(version_id)

        if not version:
            raise HTTPException(status_code=404, detail="Note not found")

        content = version.note_content
        grammar_checker = GrammarChecker()
        response = grammar_checker.check_text(content)

        return response
