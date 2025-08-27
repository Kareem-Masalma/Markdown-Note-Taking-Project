"""
This module is to create the etag used to check if the notes are updated or not when calling them.
"""
import hashlib


def generate_etag(content: str) -> str:
    """
    This method to generate etag by hashing the content of the note.
    :param content: The content of the note to be checked.
    :return: The hashed content(etag).
    """
    """Generate a strong ETag from note content."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()
