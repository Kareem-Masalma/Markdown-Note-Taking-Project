from markdown import markdown

def render_markdown_to_html(markdown_text: str) -> str:
    html = markdown(markdown_text)
    return html
