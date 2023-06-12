#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.sql.expression import tuple_

from user import Base, User


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
        Args: - email: users email
             - hashed_password: Hashed password of user
        Returns:
            - User object if user is added succesfully, otherwise None
        """
        try:
            user = User(email=email, password=hashed_password)
            self._session.add(user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            return None

        return user

    def find_user_by(self, **kwargs):
        """
        Finds user
        Arguments: **kwargs arguments
        Returns: first row found in users
        """
        fields, values = [], []
        for key, value in kwargs.items():
            if hasattr(User, key):
                fields.append(getattr(User, key))
                values.append(value)
            else:
                raise InvalidRequestError()
        result = self._session.query(User).filter(
                tuple_(*fields).in_([tuple(values)])
                ).first()
        if result is None:
            raise NoResultFound()
        return result

    def update_user(self,
                    user_id: int, **kwargs) -> None:
        """
        Updates user
        Args: - user_id(int) id to locate user by
              - **kwargs abitrary keywords
        Returns: None
        """
        user = self.find_user_by(id=user_id)

        if not user:
            return
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                raise ValueError(f"Invalid user attribute: {key}")

        self._session.commit()
        else:
            raise ValueError
