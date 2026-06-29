from enum import StrEnum


class UserQueries(StrEnum):
    CREATE_TABLE = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            user_name VARCHAR(100) NOT NULL,
            gender VARCHAR(20) NOT NULL
        );
        """
    GET_ALL = "SELECT id, user_name, gender FROM users;"
    GET_BY_ID = "SELECT id, user_name, gender FROM users WHERE id = %s;"
    EXISTS = "SELECT EXISTS(SELECT 1 FROM users WHERE id = %s);"
    ADD = (
        "INSERT INTO users (user_name, gender) VALUES (%s, %s) RETURNING"
        " id, user_name, gender;"
    )
    UPDATE = "UPDATE users SET user_name = %s, gender = %s WHERE id = %s;"
    DELETE = "DELETE FROM users WHERE id = %s;"
