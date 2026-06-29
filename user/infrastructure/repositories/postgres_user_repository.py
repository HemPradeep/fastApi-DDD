from psycopg2.extensions import connection as ConnectionType
from psycopg2.extras import RealDictCursor

from user.domain.entities.user import User
from user.domain.repositories.user_repository import UserRepository
from user.infrastructure.repositories.user_queries import UserQueries


class PostgresUserRepository(UserRepository):

    def __init__(self, conn: ConnectionType) -> None:
        self.conn = conn
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        self.create_table()

    def create_table(self) -> None:
        self.cursor.execute(UserQueries.CREATE_TABLE)
        self.conn.commit()

    def get_all(self) -> list[User]:
        self.cursor.execute(UserQueries.GET_ALL)
        rows = self.cursor.fetchall()
        return [
            User(id=row["id"], name=row["user_name"], gender=row["gender"])
            for row in rows
        ]

    def get_by_id(self, user_id: int) -> User | None:
        self.cursor.execute(UserQueries.GET_BY_ID, (user_id,))
        row = self.cursor.fetchone()
        if not row:
            return None
        return User(id=row["id"], name=row["user_name"], gender=row["gender"])

    def exists(self, user_id: int) -> bool:
        self.cursor.execute(UserQueries.EXISTS, (user_id,))
        row = self.cursor.fetchone()
        if not row:
            return False
        return bool(list(row.values())[0])

    def add(self, user: User) -> User:
        self.cursor.execute(UserQueries.ADD, (user.name, user.gender))
        row = self.cursor.fetchone()
        self.conn.commit()
        if not row:
            raise RuntimeError("failed to insert user and return row")
        return User(id=row["id"], name=row["user_name"], gender=row["gender"])

    def update(self, user: User) -> User:
        if user.id is None:
            raise ValueError("Cannot update a user without an ID")
        self.cursor.execute(UserQueries.UPDATE, (user.name, user.gender, user.id))
        self.conn.commit()
        return user

    def delete(self, user_id: int) -> None:
        self.cursor.execute(UserQueries.DELETE, (user_id,))
        self.conn.commit()
