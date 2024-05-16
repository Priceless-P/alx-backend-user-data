#!/usr/bin/env python3
"""
Regex-ing
"""
import os
from typing import List, ByteString
import re
import logging
import mysql.connector
import bcrypt

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initializes an instances of the class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Handles formatting"""
        message = super().format(record)
        return self.filter_datum(self.fields, self.REDACTION,
                                 message, self.SEPARATOR)

    @staticmethod
    def filter_datum(fields: List[str], redaction: str,
                     message: str, separator: str) -> str:
        """Returns log message obfuscated"""
        for field in fields:
            message = re.sub(f'{field}=(.*?){separator}',
                             f'{field}={redaction}{separator}', message)
        return message


def get_logger() -> logging.Logger:
    """Returns Logger"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)

    formatter = RedactingFormatter(list(PII_FIELDS))
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MYSQLConnection:
    """Connects to database"""
    connection = mysql.connector.connect(
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        database=os.getenv("PERSONAL_DATA_DB_NAME")
    )
    return connection


def main() -> None:
    """Obtains database connection and retrieve
    all rows in the users table and
    display each row under a filtered format"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")

    headers = [field[0] for field in cursor.description]
    logger = get_logger()

    for row in cursor:
        info = ""
        for data, header in zip(row, headers):
            info += "{}={}".format(header, data)
        logger.info(info)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
