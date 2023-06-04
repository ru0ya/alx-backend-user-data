#!/usr/bin/env python3
"""
Methods that encrypt password and  checks if
passowrd is valid
"""
import bcrypt


def hash_password(password: str) -> str:
    """
    Function that encrypts password using bcrypt
    Arguments: password(str)
    Returns: salted, hashed password
    """
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash_pw = bcrypt.hashpw(bytes, salt)

    return hash_pw


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Function that validates whether hashed password matches
    password
    Arguments: - hashed_password(bytes)
               - password(str)

    Returns: if matches true else false
    """
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        return True
    else:
        return False
