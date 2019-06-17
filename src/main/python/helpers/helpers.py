"""
This module contains general purpose helpers.
"""
import base64


def to_base64(utf: str) -> str:
    """ Convert a string to its base 64 encoded string. """
    bs: bytes = base64.b64encode(utf.encode())
    return bs.decode()
