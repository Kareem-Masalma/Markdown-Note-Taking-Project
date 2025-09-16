"""
This module is the FastAPI Router for users related endpoints,
it manages CRUD operations for users. Register new user, delete
available user, update user's data, read available users from
database, and Login.
"""

from fastapi import APIRouter, Depends, Query, status

from src.auth.tokens import check_token
from src.dependencies.user import get_user_service
from src.models.user import User
from src.schemas.user import UserResponse, UserRequest, UserUpdate
from src.services.user import UserService

router = APIRouter()


@router.get(
    "/",
    summary="Get all users",
    description="This endpoint returns all users available inside the database",
    response_model=list[UserResponse],
    response_description="The returned data are all the users available inside the database",
    responses={
        200: {"description": "All users returned successfully"},
        404: {"description": "No Users are found"},
    },
    status_code=status.HTTP_200_OK,
)
async def get_all_users(user_service: UserService = Depends(get_user_service)):
    """
    This endpoint is used to get all available users in the system(with delete filed set to 0).

    :param user_service: The user service to be used to get all users.
    :return: The returned value is a list of users.
    """
    users = await user_service.get_all_users()
    return users


@router.get(
    "/{username}",
    summary="Get user by username",
    description="This endpoint returns a specific user by their username",
    response_model=UserResponse,
    response_description="The returned data is a user available in the database",
    responses={
        200: {"description": "User is found"},
        404: {"description": "User not found"},
    },
    status_code=status.HTTP_200_OK,
)
async def get_user_by_username(
    username: str, user_service: UserService = Depends(get_user_service)
):
    """
    This endpoint is used to get a certain user by their username,
     the user shall be available with deleted field set to 0.

    :param username: The username, unique value for each user.
    :param user_service: The user service to be used to get the user.
    :return: The returned value is the user if found, if not a 404 HTTPException is raised.
    """
    user = await user_service.get_user_by_username(username)
    return user


@router.post(
    "/login",
    summary="Login with username and password",
    description="This endpoint for a valid user to login using username and password and returns a jwt token on success",
    response_description="The returned data is a JWT token generated on success login",
    responses={
        200: {"description": "LoggedIn Successfully"},
        404: {"description": "User not found"},
    },
    status_code=status.HTTP_200_OK,
)
async def login(
    user: UserRequest, user_service: UserService = Depends(get_user_service)
):
    """
    This endpoint is used to log in. When Logging in successfully an authorization module is called
    to generate jwt token to return it to the user.

    :param user: The user's information to log in with.
    :param user_service: The user service to be used to log in the user.
    :return: The returned value is the jwt token so the user can use to be authorized to use endpoints.
    """
    response = await user_service.login(user)
    return response


@router.post(
    "/register",
    summary="Add new user",
    description="This endpoint for registering new user not available in the database",
    response_description="The returned data is the new user added to the database",
    responses={
        200: {"description": "Added Successfully"},
        409: {"description": "User already exists"},
    },
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user: UserRequest = Query(
        ..., title="New User", description="The new user to register to database"
    ),
    user_service: UserService = Depends(get_user_service),
):
    """
    This endpoint is for creating new user, which is not available in the database even with deleted set to 0.

    :param user: The new user's information.
    :param user_service: The user service to be used to register the new user.
    :return: The new user created with its new auto generated id.
    """
    user = await user_service.register_user(user)
    return user


@router.patch(
    "/{username}",
    summary="Update user",
    description="This endpoint updates a user's data by their username",
    response_model=UserResponse,
    response_description="The returned data is the updated user",
    responses={
        200: {"description": "Updated Successfully"},
        404: {"description": "User not found"},
    },
    status_code=status.HTTP_200_OK,
)
async def update_user(
    username: str,
    user: UserUpdate,
    user_check: User = Depends(check_token),
    user_service: UserService = Depends(get_user_service),
):
    """
    This endpoint to update available user's data, the user shall be available if not HTTPException 404 is raised.

    :param username: The username of the user's data to be updated.
    :param user: The new data to update.
    :param user_check: Check if the user is authorized by the jwt token in the header.
    :param user_service: The user service to be used to update the user.
    :return: Return success if the update is done, if not 404 HTTPException.
    """
    updated_user = await user_service.update_user(username, user)
    return updated_user


@router.delete(
    "/{username}",
    summary="Delete available user",
    description="This endpoint deletes a certain user by their username",
    response_description="The returned data is a message of success",
    responses={
        200: {"description": "Deleted Successfully"},
        404: {"description": "User not found"},
    },
    status_code=status.HTTP_200_OK,
)
async def delete_user(
    username: str,
    user: User = Depends(check_token),
    user_service: UserService = Depends(get_user_service),
):
    """
    This endpoint to delete an available user from the database with deleted field set to 0.

    :param username: The username of the user's data to be deleted.
    :param user: Check if the user is authorized by the jwt token in the header.
    :param user_service: The user service to be used to delete the user.
    :return: Success message if the user is deleted, HTTPException 404 if user not found.
    """
    await user_service.delete_user(username)
    return {"success": True, "message": f"user {username} deleted"}
