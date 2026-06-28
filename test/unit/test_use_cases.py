import pytest

from application.dtos.request_objects import CreateUserRequest, UpdateUserNameRequest
from application.use_cases.create_user import CreateUserUseCase
from application.use_cases.delete_user import DeleteUserUseCase
from application.use_cases.get_user import GetAllUsersUseCase, GetUserUseCase
from application.use_cases.update_user import UpdateUserUseCase
from domain.exceptions.user_exceptions import (
    InvalidUserData,
    InvalidUserName,
    UserNotFound,
)
from infrastructure.inmemory.inmemory_user_repository import (
    InMemoryUserRepository,
)


@pytest.fixture
def user_repo() -> InMemoryUserRepository:
    return InMemoryUserRepository()


def test_create_user_success(user_repo: InMemoryUserRepository) -> None:
    use_case = CreateUserUseCase(user_repo)
    request = CreateUserRequest(user="Alice", gender="Female")

    user = use_case.execute(request)

    assert user.id == 1
    assert user.name == "Alice"
    assert user.gender == "Female"
    assert user_repo.get_by_id(1) == user


def test_create_user_invalid_data(user_repo: InMemoryUserRepository) -> None:
    use_case = CreateUserUseCase(user_repo)

    # Name with numbers
    with pytest.raises(InvalidUserData):
        use_case.execute(CreateUserRequest(user="Alice123", gender="Female"))

    # Invalid gender is handled by Pydantic, but if bypassed:
    with pytest.raises(InvalidUserData):
        # We manually test the use case level check using model_construct
        # to bypass Pydantic validation.
        use_case.execute(
            CreateUserRequest.model_construct(user="Alice", gender="Robot")
        )


def test_get_user_success(user_repo: InMemoryUserRepository) -> None:
    # Add dummy user
    from domain.entities.user import User

    existing_user = user_repo.add(User(id=None, name="Bob", gender="Male"))
    assert existing_user.id is not None

    use_case = GetUserUseCase(user_repo)
    user = use_case.execute(existing_user.id)

    assert user.id == existing_user.id
    assert user.name == "Bob"
    assert user.gender == "Male"


def test_get_user_not_found(user_repo: InMemoryUserRepository) -> None:
    use_case = GetUserUseCase(user_repo)

    with pytest.raises(UserNotFound):
        use_case.execute(999)


def test_get_all_users(user_repo: InMemoryUserRepository) -> None:
    from domain.entities.user import User

    user_repo.add(User(id=None, name="Bob", gender="Male"))
    user_repo.add(User(id=None, name="Alice", gender="Female"))

    use_case = GetAllUsersUseCase(user_repo)
    users = use_case.execute()

    assert len(users) == 2
    assert users[0].name == "Bob"
    assert users[1].name == "Alice"


def test_update_user_name_success(user_repo: InMemoryUserRepository) -> None:
    from domain.entities.user import User

    existing_user = user_repo.add(User(id=None, name="Charlie", gender="Other"))
    assert existing_user.id is not None

    use_case = UpdateUserUseCase(user_repo)
    updated = use_case.execute(
        existing_user.id, UpdateUserNameRequest(user="Charly")
    )

    assert updated.name == "Charly"
    retrieved_user = user_repo.get_by_id(existing_user.id)
    assert retrieved_user is not None
    assert retrieved_user.name == "Charly"


def test_update_user_invalid_name(user_repo: InMemoryUserRepository) -> None:
    use_case = UpdateUserUseCase(user_repo)

    with pytest.raises(InvalidUserName):
        use_case.execute(1, UpdateUserNameRequest(user="Charly123"))


def test_update_user_not_found(user_repo: InMemoryUserRepository) -> None:
    use_case = UpdateUserUseCase(user_repo)

    with pytest.raises(UserNotFound):
        use_case.execute(999, UpdateUserNameRequest(user="Charly"))


def test_delete_user_success(user_repo: InMemoryUserRepository) -> None:
    from domain.entities.user import User

    existing_user = user_repo.add(User(id=None, name="Dana", gender="Female"))
    assert existing_user.id is not None

    use_case = DeleteUserUseCase(user_repo)
    use_case.execute(existing_user.id)

    assert not user_repo.exists(existing_user.id)


def test_delete_user_not_found(user_repo: InMemoryUserRepository) -> None:
    use_case = DeleteUserUseCase(user_repo)

    with pytest.raises(UserNotFound):
        use_case.execute(999)
