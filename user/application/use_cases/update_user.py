from user.application.dtos.request_objects import UpdateUserNameRequest
from user.domain.entities.user import User
from user.domain.exceptions.user_exceptions import InvalidUserName, UserNotFound
from user.domain.repositories.user_repository import UserRepository


class UpdateUserUseCase:

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, user_id: int, request: UpdateUserNameRequest) -> User:
        if not request.user_name.isalpha():
            raise InvalidUserName("Invalid user name")

        if not self.user_repo.exists(user_id):
            raise UserNotFound(user_id)

        user = self.user_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFound(user_id)

        user.name = request.user_name
        return self.user_repo.update(user)
