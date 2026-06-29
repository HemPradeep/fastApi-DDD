class PostNotFound(Exception):
    def __init__(self, post_id: int):
        self.post_id = post_id
        super().__init__(f"Post not found: {post_id}")


class InvalidPostData(Exception):
    def __init__(self, message: str = "Invalid Post Data"):
        super().__init__(message)
