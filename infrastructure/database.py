import os

import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import connection as ConnectionType

load_dotenv()


class Database:
    _connection: ConnectionType | None = None

    @classmethod
    def get_connection(cls) -> ConnectionType:
        if cls._connection is None or cls._connection.closed:
            host = os.getenv("DB_HOST")
            database = os.getenv("DB_NAME")
            user = os.getenv("DB_USER")
            password = os.getenv("PASSWORD")

            cls._connection = psycopg2.connect(
                host=host,
                database=database,
                user=user,
                password=password,
            )
        return cls._connection

    @classmethod
    def set_connection(cls, conn: ConnectionType) -> None:
        cls._connection = conn

    @classmethod
    def close_connection(cls) -> None:
        if cls._connection is not None and not cls._connection.closed:
            cls._connection.close()
        cls._connection = None
