from psycopg2.extensions import connection as ConnectionType
from psycopg2.extras import RealDictCursor

from post.domain.entities.post import Post
from post.domain.repositories.post_repository import PostRepository
from post.infrastructure.repositories.post_queries import PostQueries


class PostgresPostRepository(PostRepository):

    def __init__(self, conn: ConnectionType) -> None:
        self.conn = conn
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        self.create_table()

    def create_table(self) -> None:
        self.cursor.execute(PostQueries.CREATE_TABLE)
        self.conn.commit()

    def add(self, post: Post) -> Post:
        self.cursor.execute(
            PostQueries.CREATE_POST, (post.author_id, post.title, post.content)
        )
        row = self.cursor.fetchone()
        if not row:
            raise RuntimeError("Failed to insert post and return row")
        return Post(
            id=row["id"],
            author_id=row["author_id"],
            title=row["title"],
            content=row["content"],
            created=row["created_at"],
            updated=row["updated_at"],
        )

    def update(self, post: Post) -> Post:
        if post.id is None:
            raise ValueError("Cannot update a post without an Id")
        self.cursor.execute(
            PostQueries.UPDATE_POST, (post.title, post.content, post.id)
        )
        self.conn.commit()
        return post

    def delete(self, post_id: int) -> None:
        self.cursor.execute(PostQueries.DELETE_POST, (post_id,))
        self.conn.commit()

    def get_all_posts(self, limit: int = 10, offset: int = 0) -> list[Post]:
        self.cursor.execute(PostQueries.GET_ALL_POSTS, (limit, offset))
        rows = self.cursor.fetchall()
        return [
            Post(
                id=row["id"],
                author_id=row["author_id"],
                title=row["title"],
                content=row["content"],
                created=row["created_at"],
                updated=row["updated_at"],
            )
            for row in rows
        ]

    def get_all_posts_by_a_user(
        self, user_id: int, limit: int = 10, offset: int = 0
    ) -> list[Post]:
        self.cursor.execute(PostQueries.GET_ALL_POSTS_BY_USER, (user_id, limit, offset))
        rows = self.cursor.fetchall()
        return [
            Post(
                id=row["id"],
                author_id=row["author_id"],
                title=row["title"],
                content=row["content"],
                created=row["created_at"],
                updated=row["updated_at"],
            )
            for row in rows
        ]

    def get_by_id(self, post_id: int) -> Post | None:
        self.cursor.execute(PostQueries.GET_POST_BY_ID, (post_id,))
        row = self.cursor.fetchone()
        if row is None:
            return None
        return Post(
            id=row["id"],
            author_id=row["author_id"],
            title=row["title"],
            content=row["content"],
            created=row["created_at"],
            updated=row["updated_at"],
        )

    def exists(self, post_id: int) -> bool:
        self.cursor.execute(PostQueries.POST_EXISTS, (post_id,))
        row = self.cursor.fetchone()
        if not row:
            return False
        return bool(list(row.values())[0])
