#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base


class DB:
    """
    DB class
    """
    def __init__(self) -> None:
        """
        Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds new user
        """
        try:
            user = User(email=email, password=hashed_password)
            self._session.add(user)
            self._session.commit()
            return user
        except Exception:
            self._session.rollback()
            return None

    def find_user_by(self, **kwargs):
        """
        Finds user
        Arguments: **kwargs arguments
        Returns: first row found in users
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()

            if user is None:
                raise NoResultFound

            return user
        except InvalidRequestError:
            raise InvalidRequestError

    def update_user(user_id: int, **kwargs) -> None:
        """
        Updates user
        Args: - user_id(int) id to locate user by
              - **kwargs abitrary keywords
        Returns: None
        """
        user = self.find_user_by(id=user_id)
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                else:
                    raise ValueError(f"Invalid user attribute: {key}")

            self._session.commit()
        else:
            raise ValueError
