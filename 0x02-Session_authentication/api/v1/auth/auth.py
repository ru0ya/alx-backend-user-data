#!/usr/bin/env python3
"""
Class to manage API authentication
"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth():
    """
    Manages API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required for a given path

        Args:
            - path: path to check for authentication requirement
            - excluded_paths: list of paths that should be excluded

        Returns:
            True if authentication is required for path else False
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path in excluded_paths or path + '/' in excluded_paths:
            return False

        for paths in excluded_paths:
            if paths.endswith('*'):
                prefix = paths.rstrip('*')
                if path.startswith(prefix):
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns None
        """
        if request is None:
            return None

        if 'Authorization' not in request.headers:
            return None

        auth_header = request.headers.get('Authorization')

        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """
        User
        """
        if request is None:
            return None

    def session_cookie(self, request=None):
        """
        Function to return a cookie request

        Arguments: request

        Returns: cookie value from request
        """
        if request is None:
            return None

        SESSION_NAME = getenv('SESSION_NAME', '_my_session_id')

        cookie = request.cookies.get(SESSION_NAME)

        return cookie
