from post.domain.exceptions.post_exceptions import PostNotFound
from post.domain.repositories.post_repository import PostRepository


class DeletePostUseCase:

    def __init__(self, post_repo: PostRepository):
        self.post_repo = post_repo

    def execute(self, post_id: int) -> None:
        if not self.post_repo.exists(post_id):
            raise PostNotFound(post_id)
        self.post_repo.delete(post_id)
