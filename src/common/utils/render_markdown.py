"""
This module is used to render any Markdown text to an HTML format using markdown library.
"""

from markdown import markdown


def render_markdown_to_html(markdown_text: str) -> str:
    """
    This method is used to render any Markdown text t an HTML format.

    :param markdown_text: The text to render.
    :return: The rendered HTML text.
    """
    html = markdown(markdown_text)
    return html
