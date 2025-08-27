import hashlib


def generate_etag(content: str) -> str:
    """Generate a strong ETag from note content."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()
