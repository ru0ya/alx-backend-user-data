#!/usr/bin/env python3
"""
Obsufication
"""

from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str):
    """
    Function that returns log message obfuscated

    Arguments:
    - fields: list of strings
    - redaction: string representing field to obfuscate
    - message: string representing log line
    - separator: string by which character is separating
    all fields in the log line

    Returns:
        Obfuscated log message
    """
    for field in fields:
        message = re.sub(f'{field}=.+?{separator}',
                         f'{field}={redaction}{separator}', message)

    return message
