from unittest.mock import Mock

from domain.entities.user import User
from infrastructure.repositories.postgres_user_repository import (
    PostgresUserRepository,
)


def build_repository() -> tuple[Mock, Mock, PostgresUserRepository]:
    conn = Mock()
    cursor = Mock()
    conn.cursor.return_value = cursor
    repo = PostgresUserRepository(conn)
    return conn, cursor, repo


def test_create_table_initializes_schema_and_commits() -> None:
    conn, cursor, _ = build_repository()

    # The table creation query is executed during __init__
    cursor.execute.assert_called_once()
    assert "CREATE TABLE IF NOT EXISTS users" in cursor.execute.call_args[0][0]
    conn.commit.assert_called_once()


def test_get_all_users_executes_query_and_returns_users() -> None:
    conn, cursor, repo = build_repository()
    # Mock RealDictCursor output
    cursor.fetchall.return_value = [{"id": 1, "user_name": "Alice", "gender": "Female"}]

    users = repo.get_all()

    # Note: call_args_list[0] is the CREATE TABLE call in __init__
    assert (
        cursor.execute.call_args_list[1][0][0]
        == "SELECT id, user_name, gender FROM users;"
    )
    cursor.fetchall.assert_called_once()
    assert len(users) == 1
    assert users[0].id == 1
    assert users[0].name == "Alice"
    assert users[0].gender == "Female"


def test_get_user_by_id_returns_matching_user() -> None:
    _, cursor, repo = build_repository()
    cursor.fetchone.return_value = {
        "id": 2,
        "user_name": "Bob",
        "gender": "Male",
    }

    user = repo.get_by_id(2)

    assert (
        cursor.execute.call_args_list[1][0][0]
        == "SELECT id, user_name, gender FROM users WHERE id = %s;"
    )
    assert cursor.execute.call_args_list[1][0][1] == (2,)
    assert user is not None
    assert user.id == 2
    assert user.name == "Bob"
    assert user.gender == "Male"


def test_get_user_by_id_returns_none_if_missing() -> None:
    _, cursor, repo = build_repository()
    cursor.fetchone.return_value = None

    user = repo.get_by_id(999)

    assert user is None


def test_exists_returns_boolean_result() -> None:
    _, cursor, repo = build_repository()
    cursor.fetchone.return_value = {"exists": True}

    assert repo.exists(3) is True
    assert (
        cursor.execute.call_args_list[1][0][0]
        == "SELECT EXISTS(SELECT 1 FROM users WHERE id = %s);"
    )
    assert cursor.execute.call_args_list[1][0][1] == (3,)


def test_add_user_inserts_and_returns_new_user() -> None:
    _, cursor, repo = build_repository()
    cursor.fetchone.return_value = {
        "id": 4,
        "user_name": "Dana",
        "gender": "Other",
    }

    user_to_add = User(id=None, name="Dana", gender="Other")
    user = repo.add(user_to_add)

    assert (
        cursor.execute.call_args_list[1][0][0]
        == "INSERT INTO users (user_name, gender) VALUES (%s, %s) RETURNING"
        " id, user_name, gender;"
    )
    assert cursor.execute.call_args_list[1][0][1] == ("Dana", "Other")
    assert user is not None
    assert user.id == 4
    assert user.name == "Dana"
    assert user.gender == "Other"


def test_update_user_executes_query_and_returns_user() -> None:
    _, cursor, repo = build_repository()

    user_to_update = User(id=5, name="Diana", gender="Female")
    user = repo.update(user_to_update)

    assert (
        cursor.execute.call_args_list[1][0][0]
        == "UPDATE users SET user_name = %s, gender = %s WHERE id = %s;"
    )
    assert cursor.execute.call_args_list[1][0][1] == ("Diana", "Female", 5)
    assert user.id == 5
    assert user.name == "Diana"
    assert user.gender == "Female"


def test_delete_user_executes_delete_query() -> None:
    _, cursor, repo = build_repository()

    repo.delete(7)

    assert cursor.execute.call_args_list[1][0][0] == "DELETE FROM users WHERE id = %s;"
    assert cursor.execute.call_args_list[1][0][1] == (7,)
