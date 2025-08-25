from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.tokens import check_token
from src.common.db.connection import Connection
from src.models.user import User
from src.schemas.user_schema import UserOut, UserIn
from src.services.user_service import UserService

router = APIRouter()


@router.get('/',
            summary="Get all users",
            description="This endpoint returns all users available inside the database",
            response_model=list[UserOut],
            response_description="The returned data are all the users available inside the database",
            responses={
                200: {"description": "All users returned successfully"},
                404: {"description": "No Users are found"}
            })
async def get_all_users(user: User = Depends(check_token), session: AsyncSession = Depends(Connection.get_session)):
    users = UserService.get_all_users(session)
    return users


@router.get('/{username}',
            summary="Get user by username",
            description="This endpoint returns a specific user by their username",
            response_model=UserOut,
            response_description="The returned data is a user available in the database",
            responses={
                200: {"description": "User is found"},
                404: {"description": "User not found"}
            })
async def get_user_by_username(username: str, user: User = Depends(check_token),
                               session: AsyncSession = Depends(Connection.get_session)):
    user = UserService.get_user_by_username(username, session)
    return user


@router.post('/login', summary="Login with username and password",
             description="This endpoint for a valid user to login using username and password and returns a jwt token on success",
             response_description="The returned data is a JWT token generated on success login",
             responses={
                 200: {"description": "LoggedIn Successfully"},
                 404: {"description": "User not found"}
             })
async def login(user: UserIn, session: AsyncSession = Depends(Connection.get_session)):
    return await UserService.signin(user, session)


@router.post('/register', summary="Add new user",
             description="This endpoint for registering new user not available in the database",
             response_description="The returned data is the new user added to the database",
             responses={
                 200: {"description": "Added Successfully"},
                 409: {"description": "User already exists"}
             })
async def register(user: UserIn = Query(..., title="New User", description="The new user to register to database"),
                   session: AsyncSession = Depends(Connection.get_session)):
    return await UserService.register_user(user, session)


@router.patch('/{username}', summary="Update user",
              description="This endpoint updates a user's data by their username",
              response_description="The returned data is the updated user",
              responses={
                  200: {"description": "Updated Successfully"},
                  404: {"description": "User not found"}
              })
async def update_user(username: str, user: UserIn, user_check: User = Depends(check_token),
                      session: AsyncSession = Depends(Connection.get_session)):
    updated_user = await UserService.update_user(username, user, session)
    return {"success": True, "user": updated_user}


@router.delete('/{username}', summary="Delete available user",
               description="This endpoint deletes a certain user by their username",
               response_description="The returned data is a message of success",
               responses={
                   200: {"description": "Deleted Successfully"},
                   404: {"description": "User not found"}
               })
async def delete_user(username: str, user: User = Depends(check_token),
                      session: AsyncSession = Depends(Connection.get_session)):
    await UserService.delete_user(username, session)
    return {'success': True, 'message': f'user {username} deleted'}
