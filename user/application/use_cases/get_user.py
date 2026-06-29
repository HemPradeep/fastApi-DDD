from user.domain.entities.user import User
from user.domain.exceptions.user_exceptions import UserNotFound
from user.domain.repositories.user_repository import UserRepository


class GetUserUseCase:

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, user_id: int) -> User:
        user = self.user_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFound(user_id)
        return user


class GetAllUsersUseCase:

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self) -> list[User]:
        return self.user_repo.get_all()
