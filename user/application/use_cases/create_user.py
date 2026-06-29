from user.application.dtos.request_objects import CreateUserRequest
from user.domain.entities.user import User
from user.domain.exceptions.user_exceptions import InvalidUserData
from user.domain.repositories.user_repository import UserRepository


class CreateUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, request: CreateUserRequest) -> User:
        if not request.user_name.isalpha() or request.gender not in [
            "Male",
            "Female",
            "Other",
        ]:
            raise InvalidUserData("Invalid user data")

        user = User(id=None, name=request.user_name, gender=request.gender)
        return self.user_repo.add(user)
