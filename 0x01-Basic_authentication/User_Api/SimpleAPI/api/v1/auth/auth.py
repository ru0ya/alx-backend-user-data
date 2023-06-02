#!/usr/bin/env python3
"""
Class to manage API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth():
    """
    Manages API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Update later
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Returns None
        """
        if request is None:
            return None

        auth_header = request.headers.get('Authorization')

        return auth_header


    def current_user(self, request=None) -> TypeVar('User'):
        """
        User
        """
        if request is None:
            return None

        user = request.users.get('User')

        return user

