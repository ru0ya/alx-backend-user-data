#!/usr/bin/env python3
"""
Authentication
"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    Hashing passwords
    Args: password(str)
    Returns: hashed password in bytes
    """
    bytes = password.encode('utf-8')

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(bytes, salt)

    return hashhed_password


def _generate_uuid() -> str:
    """
    Generates a unique id
    """
    return str(uuid.uuid4())


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
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(
                    email=email,
                    hashed_password=hashed_password
                    )

    def valid_login(email: str, password: str) -> bool:
        """
        Function to validate users credentials

        Args: - email(str): users email
              - password(str): users password
        Returns: True if user password matches else false
        """
        try:
            user = self._db.find_user_by(email=email)
            hashed_password = user.password.encode('utf-8')
            input_password = password.encode('utf-8')
            return bcrypt.checkpw(input_password, hashed_password)
        except NoResultFound:
            return False

    def _generate_uuid(self) -> str:
        """
        Calls function to genrate unique id
        """
        return _generate_uuid()

    def create_session(self, email: str) -> str:
        """
        Generares new session ID
        """
        session_id = self._generate_uuid()
        self._db.update_user(email=email, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User or None:
        """
        Finds user with corresponding session id
        """
        if session_id is None:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Updates users session id to None
        """
        self._db.update_user(user_id=user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        Finds user corresponding to provided email
        """
        user = self._db.find)_user_by(email=email)
        reset_token = _generate_uuid()
        self._db.update_user(user_id=user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Finds user corresponding to provided email
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError("Invalid reset token")

        hashed_password = _hash_password(password)
        self._db.update_user(
                user_id=user.id,
                hashed_password=hashed_password,
                reset_token=Nome
                )
