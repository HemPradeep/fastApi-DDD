from application.dtos.request_objects import CreateUserRequest
from domain.repositories.user_repository import UserRepository
from domain.entities.user import User
from domain.exceptions.user_exceptions import InvalidUserData

class CreateUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, request: CreateUserRequest) -> User:
        if not request.user.isalpha() or request.gender not in [
            "Male",
            "Female",
            "Other",
        ]:
            raise InvalidUserData("Invalid user data")

        user = User(id=None, name=request.user, gender=request.gender)
        return self.user_repo.add(user)
