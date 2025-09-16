from fastapi import HTTPException

from src.common.utils.grammar_checker import GrammarChecker
from src.models.history import History
from src.repositories.history import HistoryRepository
from src.services.issue import IssueService


class LanguageToolService:

    def __init__(
        self, history_repository: HistoryRepository, issue_service: IssueService
    ):
        self.history_repository = history_repository
        self.issue_service = issue_service

    async def check_grammar(self, version_id: int):
        """
        This method checks the grammar of a specific version of a note if found.

        :param version_id: The id of the version to check.
        :return: The issues found with the version.
        """
        try:

            version: History = await self.history_repository.get_by_id(version_id)

            if not version:
                raise HTTPException(status_code=404, detail="Note not found")

            content = version.note_content
            grammar_checker = GrammarChecker()
            issues = await grammar_checker.check_text(content)

            if issues and len(issues) > 0:
                for issue in issues:
                    await self.issue_service.create_issue(issue, version_id)

            return issues

        except Exception as e:
            raise e
