from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from post.application.dtos.request_objects import CreatePostRequest, UpdatePostRequest
from post.application.use_cases.create_post import CreatePostUseCase
from post.application.use_cases.delete_post import DeletePostUseCase
from post.application.use_cases.get_post import (
    GetAllPostsUseCase,
    GetPostByUserUseCase,
    GetPostUseCase,
)
from post.application.use_cases.update_post import UpdatePostUseCase
from post.domain.repositories.post_repository import PostRepository
from post.infrastructure.repositories.postgres_post_repository import (
    PostgresPostRepository,
)
from shared.infrastructure.database_connection import Database
from user.domain.repositories.user_repository import UserRepository
from user.presentation.controllers.user_controller import get_user_repository

router = APIRouter(tags=["Posts"])


def get_post_repository() -> PostRepository:
    conn = Database.get_connection()
    return PostgresPostRepository(conn)


def get_create_post_use_case(
    repo: Annotated[PostRepository, Depends(get_post_repository)],
) -> CreatePostUseCase:
    return CreatePostUseCase(repo)


def get_delete_post_use_case(
    repo: Annotated[PostRepository, Depends(get_post_repository)],
) -> DeletePostUseCase:
    return DeletePostUseCase(repo)


def get_update_post_use_case(
    repo: Annotated[PostRepository, Depends(get_post_repository)],
) -> UpdatePostUseCase:
    return UpdatePostUseCase(repo)


def get_get_post_use_case(
    repo: Annotated[PostRepository, Depends(get_post_repository)],
) -> GetPostUseCase:
    return GetPostUseCase(repo)


def get_get_all_posts_use_case(
    repo: Annotated[PostRepository, Depends(get_post_repository)],
) -> GetAllPostsUseCase:
    return GetAllPostsUseCase(repo)


def get_get_posts_by_user_use_case(
    post_repo: Annotated[PostRepository, Depends(get_post_repository)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> GetPostByUserUseCase:
    return GetPostByUserUseCase(post_repo, user_repo)


@router.post(
    "/users/{user_id}/posts",
    status_code=status.HTTP_201_CREATED,
)
def create_post(
    user_id: int,
    request: CreatePostRequest,
    use_case: Annotated[
        CreatePostUseCase,
        Depends(get_create_post_use_case),
    ],
):
    return use_case.execute(user_id=user_id, request=request)


@router.get("/users/{user_id}/posts")
def get_posts_by_user(
    user_id: int,
    use_case: Annotated[
        GetPostByUserUseCase,
        Depends(get_get_posts_by_user_use_case),
    ],
):
    return use_case.execute(user_id)


@router.get("/posts")
def get_all_posts(
    use_case: Annotated[
        GetAllPostsUseCase,
        Depends(get_get_all_posts_use_case),
    ],
    limit: int = Query(default=10, ge=1),
    offset: int = Query(default=0, ge=0),
):
    print(limit, type(limit))
    return use_case.execute(limit=limit, offset=offset)


@router.get("/posts/{post_id}")
def get_post(
    post_id: int,
    use_case: Annotated[
        GetPostUseCase,
        Depends(get_get_post_use_case),
    ],
):
    return use_case.execute(post_id)


@router.put("/posts/{post_id}")
def update_post(
    post_id: int,
    request: UpdatePostRequest,
    use_case: Annotated[
        UpdatePostUseCase,
        Depends(get_update_post_use_case),
    ],
):
    return use_case.execute(post_id=post_id, request=request)


@router.delete(
    "/posts/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_post(
    post_id: int,
    use_case: Annotated[
        DeletePostUseCase,
        Depends(get_delete_post_use_case),
    ],
):
    use_case.execute(post_id)
