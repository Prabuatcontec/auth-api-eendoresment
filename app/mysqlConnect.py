import MySQLdb
import json
from dotenv import load_dotenv

import os

load_dotenv()


class Connection:
    def __init__(self):
        MYSQL_USER = os.getenv("MYSQL_USER")
        MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
        MYSQL_DB = os.getenv("MYSQL_DB")
        MYSQL_URL = os.getenv("MYSQL_URL")
        self.db = MySQLdb.connect(
            MYSQL_URL,
            MYSQL_USER,
            MYSQL_PASSWORD,
            MYSQL_DB
        )
        self.db.autocommit(True)
        self.db.set_character_set('utf8mb4')
        self.cur = self.db.cursor()