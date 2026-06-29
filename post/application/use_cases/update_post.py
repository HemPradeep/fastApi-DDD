from post.application.dtos.request_objects import UpdatePostRequest
from post.domain.entities.post import Post
from post.domain.exceptions.post_exceptions import PostNotFound
from post.domain.repositories.post_repository import PostRepository


class UpdatePostUseCase:

    def __init__(self, post_repo: PostRepository):
        self.post_repo = post_repo

    def execute(self, post_id: int, request: UpdatePostRequest) -> Post:
        post = self.post_repo.get_by_id(post_id)
        if post is None:
            raise PostNotFound(post_id)
        post.title = request.title
        return self.post_repo.update(post)
