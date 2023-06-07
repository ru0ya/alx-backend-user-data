#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from asqlalchemy.ext.declarative import declarative_base
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
        self.__session = sessionmaker(bind=self._engine)

    @property
    def _session(self) -> Session:
        """
        Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__sesson = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds new user
        """
        session = self.Session()
        user = User(email=email, password=hashed_password)
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs):
        """
        Finds user
        Arguments: **kwargs arguments
        Returns: first row found in users
        """
        try:
            user = self.session.query(User).filter_by(**kwargs).first()

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
                setattr(user, key, value)

            self.session.commit()
        else:
            raise ValueError
