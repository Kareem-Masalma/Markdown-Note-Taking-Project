"""
This module contains grammar checker using LanguageTool public API.
"""

import httpx
from typing import Dict, Any, List


class GrammarChecker:
    def __init__(self, base_url: str = "https://api.languagetool.org/v2/check"):
        self.base_url = base_url

    async def check_text(
        self, text: str, language: str = "en-US"
    ) -> List[Dict[str, Any]]:
        """
        This method is used to do a grammar check on a certain text with a chosen language, it sends a post request to
        languagetool public api url.

        :param text: The text to check.
        :param language: The language of the text.
        :return: A list of dictionaries containing the results of the check. (Error message, context, offset, length,
        suggestions, category, type).
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url, data={"text": text, "language": language}
            )
            response.raise_for_status()
            data = response.json()

        issues = []
        for match in data.get("matches", []):
            issues.append(
                {
                    "message": match["message"],
                    "context": match["context"]["text"],
                    "offset": match["offset"],
                    "length": match["length"],
                    "suggestions": [r["value"] for r in match.get("replacements", [])],
                    "category": match.get("rule", {}).get("category", {}).get("name"),
                    "type": match.get("rule", {}).get("issueType"),
                }
            )
        return issues
