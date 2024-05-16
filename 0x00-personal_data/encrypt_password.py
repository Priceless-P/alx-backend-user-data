#!/usr/bin/env python3
"""
Password encryption
"""
from typing import ByteString
import bcrypt


def hash_password(password: str) -> ByteString:
    """Hashes password"""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if password is valid"""
    password_bytes = password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_password)
