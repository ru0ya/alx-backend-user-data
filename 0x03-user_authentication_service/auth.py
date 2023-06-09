#!/usr/bin/env python3
"""
Authentication
"""
import bcrypt
from db import DB


def _hash_password(password: str) -> bytes:
    """
    Hashing passwords
    Args: password(str)
    Returns: hashed password in bytes
    """
    bytes = password.encode('utf-8')

    salt = bcrypt.gensalt()

    hash = bcrypt.hashpw(bytes, salt)

    return hash


class Auth:
    """
    Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def register_user(email: str, password: str) -> User:
        """
        Registers users using email

        Args:
            - email(str)
            - password(str)
        Returns: User
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(
                    email,
                    self._hash_password(password)
                    )
        raise ValueError("User {} already exists".format(email))

    def valid_login(email: str, password: str) -> bool:
        """
        Function to validate users credentials

        Args: - email(str): users email
              - password(str): users password
        Returns: True if user password matches else false
        """
        pass
