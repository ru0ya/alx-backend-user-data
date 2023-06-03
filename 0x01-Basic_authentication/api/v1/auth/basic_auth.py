#!/usr/bin/env python3
"""
Class that inherits from Auth
"""

import base64
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """
    Child class that inherits from Auth
    """
    def extract_base64_authorization_header(
                                            self,
                                            authorization_header: str
                                            ) -> str:
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

        auth_headers = authorization_header.split(' ')[1]

        return auth_headers

    def decode_base64_authorization_header(
                                           self,
                                           base64_authorization_header: str
                                           ) -> str:
        """
        Arguments: base64_authorization_header(str)
        Returns:
            - decoded value of a Base64 string
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            encode_header = base64_authorization_header.encode('utf-8')
            decoded_header = base64.b64decode(encode_header)
            return decoded_header.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
                                 self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """
        Arguments: decoded_base64_authorization_header(str)

        Returns:
            - User email and password from Base64 decoded value
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        split_values = decoded_base64_authorization_header.split(":")
        email = split_values[0]
        password = ":".join(split_values[1:])

        return email, password

    def user_object_from_credentials(
                                     self,
                                     user_email: str,
                                     user_pwd: str
                                     ) -> TypeVar('User'):
        """
        Arguments:
                - user_email(str)
                - user_pwd(str)

        Returns: User instance based on his email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        users = User.search({"email": user_email})

        if user_email != users:
            return None

        user = users[0]
        password = User.is_valid_password(user.password, user_pwd)

        if not password:
            return None

        return User.user

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Overloads Class Auth and retrieves User instance
        for a request

        Arguments: request

        Returns: User instance based on recieved request
        """
        auth_header = self.authorization_header(request)
        if auth_header is not None:
            base64_header = self.extract_base64_authorization_header(
                    auth_header)
            if base64_header is not None:
                decoded_header = self.decode_base64_authorization_header(
                        base64_header)
                if decoded_header is not None:
                    email, passwd = self.extract_user_credentials(decoded)
                    if email is not None:
                        return self.user_object_from_credentials(email, passwd)
        return
