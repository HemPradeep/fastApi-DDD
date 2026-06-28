import os
from collections.abc import Generator
from typing import Any

import psycopg2
import pytest
from fastapi.testclient import TestClient
from psycopg2.extensions import connection

from infrastructure.repositories.postgres_user_repository import PostgresUserRepository
from main import app
from presentation.controllers.user_controller import get_user_repository


def get_test_connection() -> connection:
    return psycopg2.connect(
        host=os.getenv("TEST_DB_HOST"),
        database=os.getenv("TEST_DB_NAME"),
        user=os.getenv("TEST_DB_USER"),
        password=os.getenv("TEST_DB_PASSWORD"),
    )


def reset_database(conn: connection) -> None:
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM users;")
        try:
            cursor.execute(
                "SELECT setval(pg_get_serial_sequence('users', 'id'), 1, false);"
            )
        except Exception:
            pass
    conn.commit()


@pytest.fixture
def client() -> Generator[TestClient, Any, None]:
    conn = get_test_connection()
    repository = PostgresUserRepository(conn)
    reset_database(conn)
    app.dependency_overrides[get_user_repository] = lambda: repository
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    conn.close()


def test_listing_all_users_returns_empty_collection(client: TestClient) -> None:
    response = client.get("/api/users")

    assert response.status_code == 200
    assert response.json() == []


def test_create_user_returns_created_user(client: TestClient) -> None:
    response = client.post(
        "/api/users",
        json={"user": "Hem", "gender": "Male"},
    )

    assert response.status_code == 201
    assert response.json() == {"id": 1, "user": "Hem", "gender": "Male"}


def test_get_user_by_id_returns_existing_user(client: TestClient) -> None:
    client.post("/api/users", json={"user": "Bob", "gender": "Male"})

    response = client.get("/api/users/1")

    assert response.status_code == 200
    assert response.json() == {"id": 1, "user": "Bob", "gender": "Male"}


def test_update_user_changes_name(client: TestClient) -> None:
    client.post("/api/users", json={"user": "Charlie", "gender": "Other"})

    response = client.put("/api/users/1", json={"user": "Charly"})

    assert response.status_code == 200
    assert response.json()["user"] == "Charly"


def test_delete_user_removes_the_user(client: TestClient) -> None:
    client.post("/api/users", json={"user": "Dana", "gender": "Female"})

    response = client.delete("/api/users/1")

    assert response.status_code == 204
    assert client.get("/api/users/1").status_code == 404


def test_create_user_rejects_invalid_payload(client: TestClient) -> None:
    response = client.post(
        "/api/users",
        json={"user": "Alice123", "gender": "Female"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid user data"


def test_get_user_by_id_returns_404_for_missing_user(client: TestClient) -> None:
    response = client.get("/api/users/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "invalid userId: 999"
