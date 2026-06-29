from abc import ABC, abstractmethod

from post.domain.entities.post import Post


class PostRepository(ABC):
    @abstractmethod
    def add(self, post: Post) -> Post:
        pass

    @abstractmethod
    def update(self, post: Post) -> Post:
        pass

    @abstractmethod
    def delete(self, post_id: int) -> None:
        pass

    @abstractmethod
    def get_by_id(self, post_id: int) -> Post | None:
        pass

    @abstractmethod
    def get_all_posts(self, limit: int = 0, offset: int = 20) -> list[Post]:
        pass

    @abstractmethod
    def exists(self, post_id: int) -> bool:
        pass

    @abstractmethod
    def get_all_posts_by_a_user(
        self, user_id: int, limit: int = 0, offset: int = 20
    ) -> list[Post]:
        pass
