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
        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith('Basic '):
            return None

        auth_headers = authorization_header.split('Basic', 1)
        if len(auth_headers) != 2:
            return None

        return auth_headers[1]

    
    def decode_base64_authorization_header(self, 
                base64_authorization_header: str) -> str:
        """
        Arguments: base64_authorization_header(str)
        Returns:
            - decoded value of a Base64 string
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
