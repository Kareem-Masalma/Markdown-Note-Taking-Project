"""
This module is used to manage passwords, hash, and verify password on login.
It uses CryptContext to hash and verify.
"""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    This method hashes the password before adding it to the database.

    :param password: The password to be hashed.
    :return: The hashed password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    This method used to verify password when logging in.
    :param plain_password: The password entered on log in.
    :param hashed_password: The password stored in the database
    :return: True if they match, else it returns False.
    """
    return pwd_context.verify(plain_password, hashed_password)
