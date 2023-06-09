#!/usr/bin/env python3
"""
Obsufication
"""

import logging
import re
import os
import bcrypt
from typing import List
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")
PERSONAL_DATA_DB_USERNAME = "root"
PERSONAL_DATA_DB_PASSWORD = " "
PERSONAL_DATA_DB_HOST = "localhost"


def get_db():
    """
    Function that returns a connector to the database
    """
    username = os.get_env("PERSONAL_DATA_DB_USERNAME")
    password = os.get_env("PERSONAL_DATA_DB_PASSWORD")
    host = os.get_env("PERSONAL_DATA_DB_HOST")

    PERSONAL_DATA_DB_NAME = mysql.connector.connect(
            host, username, password)


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
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
        Constructor method
        Args:
            - fields: list of fields to redact in log messages
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


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Function that fetches database credentials
    """
    user = os.getenv('PERSONAL_DATA_DB_USERNAME') or "root"
    passwd = os.getenv('PERSONAL_DATA_DB_PASSWORD') or ""
    host = os.getenv('PERSONAL_DATA_DB_HOST') or "localhost"
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')
    conn = mysql.connector.connect(user=user,
                                   password=passwd,
                                   host=host,
                                   database=db_name)
    return conn
