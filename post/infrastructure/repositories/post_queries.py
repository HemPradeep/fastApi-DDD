from enum import StrEnum


class PostQueries(StrEnum):
    CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS posts (
        id SERIAL PRIMARY KEY,
        author_id INTEGER NOT NULL,
        title VARCHAR(255) NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """

    CREATE_POST = """
    INSERT INTO posts (
        author_id,
        title,
        content
    )
    VALUES (%s, %s, %s)
    RETURNING *;
    """

    GET_POST_BY_ID = """
    SELECT
        id,
        author_id,
        title,
        content,
        created_at,
        updated_at
    FROM posts
    WHERE id = %s;
    """

    GET_ALL_POSTS = """
    SELECT
        id,
        author_id,
        title,
        content,
        created_at,
        updated_at
    FROM posts
    ORDER BY created_at DESC
    LIMIT %s OFFSET %s;
    """

    GET_ALL_POSTS_BY_USER = """
    SELECT
        id,
        author_id,
        title,
        content,
        created_at,
        updated_at
    FROM posts
    WHERE author_id = %s
    ORDER BY created_at DESC
    LIMIT %s OFFSET %s;
    """

    UPDATE_POST = """
    UPDATE posts
    SET
        title = %s,
        content = %s,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = %s
    RETURNING *;
    """

    DELETE_POST = """
    DELETE FROM posts
    WHERE id = %s;
    """

    POST_EXISTS = """
    SELECT EXISTS(
        SELECT 1
        FROM posts
        WHERE id = %s
    );
    """
