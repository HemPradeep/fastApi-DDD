from post.application.dtos.request_objects import CreatePostRequest
from post.domain.entities.post import Post
from post.domain.repositories.post_repository import PostRepository


class CreatePostUseCase:
    def __init__(self, post_repo: PostRepository):
        self.post_repo = post_repo

    def execute(self, user_id: int, request: CreatePostRequest) -> Post:
        post = Post(
            id=None,
            author_id=user_id,
            title=request.title,
            content=request.content,
            created=None,
            updated=None,
        )
        return self.post_repo.add(post)
