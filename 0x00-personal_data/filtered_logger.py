#!/usr/bin/env python3
"""
Obsufication
"""

import logging
import re
from typing import List


PII_FIELDS = ["name", "email", "phone", "ssn", "password"]


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


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        """
        Accepts a list of strings fields constructor argument
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Filters values in incoming log records using filter_datum

        Arguments:
                - record: Log record of an event
        Returns:
                - formatted log message
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)

        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """
    Creates a logger and disables the propagation
    of log messages from this logger to higher-level
    loggers
    Arguments: None
    Returns: A logging.Logger object
    """
    log = logging.getLogger("user_data")
    log.propagate = False
    log.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    handler.setFormatter(formatter)

    log.addHandler(handler)

    return log






