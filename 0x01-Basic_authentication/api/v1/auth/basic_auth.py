#!/usr/bin/env python3
"""Basic Auth Class
"""
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User
import base64


class BasicAuth(Auth):
    """Implements Basic Access
    Authentication"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Returns Base64 part of Authorization header"""
        if authorization_header is None or \
                not isinstance(authorization_header, str)\
                or not authorization_header.startswith("Basic "):
            return None
        string = authorization_header.split(" ")
        return string[-1]

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """Returns user and password from
        the Base64 decoded value."""
        if decoded_base64_authorization_header is None or \
                not isinstance(decoded_base64_authorization_header, str)\
                or not decoded_base64_authorization_header.__contains__(":"):
            return (None, None)

        details = decoded_base64_authorization_header.split(":")
        username = details[0]
        password = details[1]
        return (username, password)

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """Returns the decoded value of a Base64 string"""
        if base64_authorization_header is None or \
           not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Returns a user given his/her email
        and password"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        user = User()
        user = user.search(attributes={"email": user_email})

        if not user:
            return None

        user = user[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the User instance for a request"""
        authorization = self.authorization_header(request)
        extract_auth = self.extract_base64_authorization_header(authorization)
        decoded_auth = self.decode_base64_authorization_header(extract_auth)
        user_cred = self.extract_user_credentials(decoded_auth)
        user = self.user_object_from_credentials(user_cred[0], user_cred[1])
        return user
