from post.domain.entities.post import Post
from post.domain.exceptions.post_exceptions import PostNotFound
from post.domain.repositories.post_repository import PostRepository
from user.domain.exceptions.user_exceptions import UserNotFound
from user.domain.repositories.user_repository import UserRepository


class GetPostUseCase:

    def __init__(self, post_repo: PostRepository):
        self.post_repo = post_repo

    def execute(self, post_id: int) -> Post:
        post = self.post_repo.get_by_id(post_id)
        if post is None:
            raise PostNotFound(post_id)
        return post


class GetAllPostsUseCase:

    def __init__(self, post_repo: PostRepository):
        self.post_repo = post_repo

    def execute(self, limit: int = 10, offset: int = 0) -> list[Post]:
        return self.post_repo.get_all_posts(
            limit=10,
        )


class GetPostByUserUseCase:

    def __init__(self, post_repo: PostRepository, user_repo: UserRepository):
        self.post_repo = post_repo
        self.user_repo = user_repo

    def execute(self, user_id: int, limit: int = 10, offset: int = 0):
        if not self.user_repo.exists(user_id):
            raise UserNotFound(user_id)
        return self.post_repo.get_all_posts_by_a_user(user_id, limit, offset)
