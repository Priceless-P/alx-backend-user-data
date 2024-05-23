#!/usr/bin/env python3
"""Auth Class
"""
import os
from typing import List, TypeVar
from flask import request


class Auth:
    """Class is the template for
    all authentication system"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Defines paths that does not need auth"""
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        if not path.endswith("/"):
            path += "/"

        for excluded_path in excluded_paths:
            if not excluded_path.endswith('/'):
                excluded_path += "/"
            if path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Checks headers for authorization"""
        if request is not None:
            return request.headers.get("Authorization", None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns current User"""
        return None

    def session_cookie(self, request=None):
        """Returns a cookie from request"""
        if request is None:
            return None
        cookie_name = os.getenv('SESSION_NAME')
        return request.cookies.get(cookie_name)
