from typing import Annotated

from fastapi import APIRouter, Depends, status

from shared.infrastructure.database_connection import Database
from user.application.dtos.request_objects import (
    CreateUserRequest,
    UpdateUserNameRequest,
)
from user.application.dtos.response_objects import UserResponse
from user.application.use_cases.create_user import CreateUserUseCase
from user.application.use_cases.delete_user import DeleteUserUseCase
from user.application.use_cases.get_user import GetAllUsersUseCase, GetUserUseCase
from user.application.use_cases.update_user import UpdateUserUseCase
from user.domain.entities.user import User
from user.domain.repositories.user_repository import UserRepository
from user.infrastructure.repositories.postgres_user_repository import (
    PostgresUserRepository,
)

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_repository() -> UserRepository:
    conn = Database.get_connection()
    return PostgresUserRepository(conn)


def get_create_user_use_case(
    repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> CreateUserUseCase:
    return CreateUserUseCase(repo)


def get_get_user_use_case(
    repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> GetUserUseCase:
    return GetUserUseCase(repo)


def get_get_all_users_use_case(
    repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> GetAllUsersUseCase:
    return GetAllUsersUseCase(repo)


def get_update_user_use_case(
    repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> UpdateUserUseCase:
    return UpdateUserUseCase(repo)


def get_delete_user_use_case(
    repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> DeleteUserUseCase:
    return DeleteUserUseCase(repo)


def to_user_response(user: User) -> UserResponse:
    assert user.id is not None
    assert user.name is not None
    assert user.gender in ("Male", "Female", "Other")
    return UserResponse(
        id=user.id,
        user_name=user.name,
        gender=user.gender,
    )


@router.get("", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def get_all_users(
    use_case: Annotated[GetAllUsersUseCase, Depends(get_get_all_users_use_case)],
) -> list[UserResponse]:
    users = use_case.execute()
    return [to_user_response(u) for u in users]


@router.get("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user_by_id(
    id: int,
    use_case: Annotated[GetUserUseCase, Depends(get_get_user_use_case)],
) -> UserResponse:
    user = use_case.execute(id)
    return to_user_response(user)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def add_a_user(
    request: CreateUserRequest,
    use_case: Annotated[CreateUserUseCase, Depends(get_create_user_use_case)],
) -> UserResponse:
    user = use_case.execute(request)
    return to_user_response(user)


@router.put("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(
    id: int,
    request: UpdateUserNameRequest,
    use_case: Annotated[UpdateUserUseCase, Depends(get_update_user_use_case)],
) -> UserResponse:
    user = use_case.execute(id, request)
    return to_user_response(user)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    id: int,
    use_case: Annotated[DeleteUserUseCase, Depends(get_delete_user_use_case)],
) -> None:
    use_case.execute(id)
