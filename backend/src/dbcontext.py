import sqlite3
from src.config import Config


class Database:
    def __init__(self) -> None:
        self.conn = sqlite3.connect(Config.Path.Db.db)
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()
