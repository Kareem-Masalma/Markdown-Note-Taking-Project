from typing import Dict, Any

from src.models.issue import Issue
from src.repositories.issue_repositoy import IssueRepository


class IssueService:
    def __init__(self, issue_repository: IssueRepository):
        self.issue_repository = issue_repository

    async def create_issue(self, issue: Dict[str, Any]):
        try:
            issue = Issue(context=issue['context'], offset=issue['offset'], length=issue['length'],
                          error_message=issue['message'],
                          error_category=issue['category'], error_type=issue['type'], suggestion=issue['suggestions'])

            res = await self.issue_repository.create(issue)
            return res
        except Exception as e:
            raise e
