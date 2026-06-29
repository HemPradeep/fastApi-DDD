from user.domain.exceptions.user_exceptions import UserNotFound
from user.domain.repositories.user_repository import UserRepository


class DeleteUserUseCase:

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, user_id: int) -> None:
        if not self.user_repo.exists(user_id):
            raise UserNotFound(user_id)
        self.user_repo.delete(user_id)
