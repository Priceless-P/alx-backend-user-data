#!/usr/bin/env python3
"""Auth Class
"""
from typing import List, TypeVar
from flask import request


class Auth:
    """Class is the template for
    all authentication system"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Defines paths that does not need auth"""
        return False

    def authorization_header(self, request=None) -> str:
        """Checks auth headers"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns current User"""
