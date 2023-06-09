#!/usr/bin/env python3
"""
Class that inherits from Auth to
create a new authentication mechanism
"""

from api.v1.auth.auth import Auth
from api.v1.views import app_views
import uuid


class SessionAuth(Auth):
    """
    - Validates if everything inherits correctly without
      overloading
    - validates the 'switch' using env variables
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Method that creates a session ID for a user_id

        Arguments: user_id(str)

        Returns: session ID using uuid
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        id = uuid.uuid4()

        self.user_id_by_session_id[id] = user_id

        return id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Function that returns a user id based on session id

        Arguments: session_id(str)

        Returns: User
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        users_id = self.user_id_by_session_id.get(session_id)

        return users_id

    def current_user(self, request=None):
        """
        Function that returns User instance based on a cookie value

        Arguments: request

        Returns: User instance based on cookie value
        """
        cookie = self.session_cookie(request)
        if cookie is None:
            return None
        user_id = self.user_id_for_session_id(cookie)
        if user_id is None:
            return None
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """
        Function that deletes user session

        Args: request

        Returns:
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        del self.user_id_by_session_id[session_id]
        return True
