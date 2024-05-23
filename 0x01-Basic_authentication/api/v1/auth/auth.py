#!/usr/bin/env python3
"""Auth Class
"""
import fnmatch
from typing import List, TypeVar
from flask import request


class Auth:
    """Class is the template for
    all authentication system"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Defines paths that does not need auth"""
        if path is None or excluded_paths is None or not excluded_paths:
            return True
        for excluded_path in excluded_paths:
            if fnmatch(path, excluded_path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Checks auth headers"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns current User"""
