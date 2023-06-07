#!/usr/bin/env python3
"""
Authentication System
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()


class User(Base):
    """
    users
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    session_id = Column(String, nullable=True)
    reset_token = Column(String, nullable=False)

    def __repr__(self):
        return (f"<User(id={self.id}, email='{self.email}', "
                f"hashed_password='{self.hashed_password}', "
                f"session_id='{self.session_id}', "
                f"reset_token='{self.reset_token}')>")
