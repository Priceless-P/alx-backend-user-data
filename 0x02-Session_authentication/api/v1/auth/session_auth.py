#!/usr/bin/env python3
"""Session Auth Class
"""
from api.v1.auth.auth import Auth
from uuid import uuid4
from api.v1.views.users import User


class SessionAuth(Auth):
    """Implements Session Access
    Authentication"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates session ID for user_id"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a user id based on session id"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Returns a User instance based on a cookie value"""
        session_id = self.session_cookie(request)
        if session_id is None:
            return None
        user_id = self.user_id_for_session_id(session_id)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """Deletes the user session / logout"""
        if request is None:
            return False
        session_ID_cookie = self.session_cookie(request)
        if not session_ID_cookie:
            return False
        user_id = self.user_id_for_session_id(session_ID_cookie)
        if not user_id:
            return False
        try:
            del self.user_id_by_session_id[session_ID_cookie]
        except Exception:
            pass
        return True
