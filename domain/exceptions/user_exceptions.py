class UserAlreadyExists(Exception):

    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"User already exists: {user_id}")


class UserNotFound(Exception):

    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"invalid userId: {user_id}")


class InvalidUserData(Exception):

    def __init__(self, message: str = "Invalid user data"):
        super().__init__(message)


class InvalidUserName(Exception):

    def __init__(self, message: str = "Invalid user name"):
        super().__init__(message)
