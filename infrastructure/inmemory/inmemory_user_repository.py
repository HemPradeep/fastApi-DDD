from domain.entities.user import User
from domain.repositories.user_repository import UserRepository


class InMemoryUserRepository(UserRepository):

    def __init__(self) -> None:
        self.users: dict[int, User] = {}
        self.next_id: int = 1

    def get_all(self) -> list[User]:
        return list(self.users.values())

    def get_by_id(self, user_id: int) -> User | None:
        return self.users.get(user_id)

    def exists(self, user_id: int) -> bool:
        return user_id in self.users

    def add(self, user: User) -> User:
        user_id = self.next_id
        self.next_id += 1
        new_user = User(id=user_id, name=user.name, gender=user.gender)
        self.users[user_id] = new_user
        return new_user

    def update(self, user: User) -> User:
        if user.id is None or user.id not in self.users:
            raise ValueError("User not found or ID is missing")
        self.users[user.id] = user
        return user

    def delete(self, user_id: int) -> None:
        if user_id in self.users:
            del self.users[user_id]
