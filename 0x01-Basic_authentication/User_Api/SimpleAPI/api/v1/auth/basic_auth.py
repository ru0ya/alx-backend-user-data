#!/usr/bin/env python3
"""
Class that inherits from Auth
"""

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    Child class that inherits from Auth
    """
    def extract_base64_authorization_header(self,
                            authorization_header: str) -> str:
        """
        Arguments: authorization_header(str)
        Returns:
            - Base64 part of the Authorization header
        """
        if authorization_header is None:
            return None
        if type(authorization_header) not str:
            return None


