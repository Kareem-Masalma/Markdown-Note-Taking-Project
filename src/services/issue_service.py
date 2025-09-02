from typing import Dict, Any

from fastapi import HTTPException

from src.models.history import History
from src.models.issue import Issue
from src.repositories.history_repository import HistoryRepository
from src.repositories.issue_repositoy import IssueRepository


class IssueService:
    def __init__(self, issue_repository: IssueRepository):
        self.issue_repository = issue_repository

    async def create_issue(self, issue: Dict[str, Any], version_id: int):
        """
        This method create an issue to the database.

        :param version_id: The id of the version of the note.
        :param issue: The issue to add.
        :return: The added issue.
        """
        try:
            issue = Issue(
                context=issue["context"],
                offset=issue["offset"],
                length=issue["length"],
                error_message=issue["message"],
                error_category=issue["category"],
                error_type=issue["type"],
                suggestion=issue["suggestions"],
                version_id=version_id,
            )

            res = await self.issue_repository.create(issue)
            return res
        except Exception as e:
            raise e

    async def fix_issue(self, issue_id: int):
        issue: Issue = await self.issue_repository.get_by_id(issue_id)

        if not issue:
            raise HTTPException(status_code=404, detail="Issue not found")

        if issue.fixed:
            raise HTTPException(status_code=400, detail="Issue already fixed")

        history_repository = HistoryRepository(self.issue_repository.session)

        version: History = await history_repository.get_version_by_id(issue.version_id)

        text = version.note_content
        suggestion = issue.suggestion
        start = issue.offset
        end = start + issue.length
        fixed_text = text[:start] + suggestion + text[end]
        version.note_content = fixed_text
        issue.fixed = 1

        await history_repository.update_version(version)
        await self.issue_repository.update_issue(issue)

        return version

    async def version_issues(self, version_id: int):
        issues: list[Issue] = await self.issue_repository.get_version_issues(version_id)

        if not issues:
            raise HTTPException(status_code=404, detail="Issues not found")

        return issues
