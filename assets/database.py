import sqlite3
import time
import threading
import os
from abc import ABC, abstractmethod

class AbstractDB(ABC):
    _conn = None
    _cursor = None
    @classmethod
    @abstractmethod
    def get_db_file(cls) -> str:
        pass

    @classmethod
    def connect(cls) -> None:
        if cls._conn is None:
            cls._conn = sqlite3.connect(cls.get_db_file(), check_same_thread=False)
            cls._cursor = cls._conn.cursor()

    @classmethod
    def query(cls, sql, params=()) -> [()]:
        cls._cursor.execute(sql, params)
        return cls._cursor.fetchall()

    @classmethod
    def execute(cls, sql, params=()) -> None:
        cls._cursor.execute(sql, params)
        cls._conn.commit()

    @classmethod
    def execute_script(cls, sql_script: str) -> None:
        cls._cursor.executescript(sql_script)
        cls._conn.commit()

    @classmethod
    def close(cls) -> None:
        if cls._conn:
            cls._conn.close()
            cls._conn = None
            cls._cursor = None

class MainDB(AbstractDB):
    @classmethod
    def get_db_file(cls) -> str:
        return os.environ.get("TIMELINE_DATABASE")

class LoggingDB(AbstractDB):
    @classmethod
    def get_db_file(cls) -> str:
        return os.environ.get("INTERNAL_DATABASE")
