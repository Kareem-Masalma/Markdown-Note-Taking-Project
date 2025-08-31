from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.tokens import check_token
from src.common.db.connection import Connection
from src.models.user import User
from src.repositories.tag_repository import TagRepository
from src.schemas.tag_schema import TagOut, TagIn
from src.services.tag_service import TagService

router = APIRouter()


@router.get("/",
            summary="Get all tags.",
            description="This endpoint return all tags if available inside the database",
            response_model=list[TagOut],
            response_description="The returned data are the requested tags",
            responses={
                200: {"description": "The tags requested returned successfully"},
                404: {"description": "No tags were found"},
            },
            status_code=status.HTTP_200_OK, )
async def get_all_tags(
        user: User = Depends(check_token),
        session: AsyncSession = Depends(Connection.get_session),
):
    tag_service = TagService(TagRepository(session))
    tags = await tag_service.get_all_tags()
    return tags


@router.get(
    "/{tag_id}",
    summary="Get tag by its id",
    description="This endpoint return a tag if available inside the database",
    response_model=TagOut,
    response_description="The returned data is the requested tag",
    responses={
        200: {"description": "The tag requested returned successfully"},
        404: {"description": "Tag not found"},
    },
    status_code=status.HTTP_200_OK,
)
async def get_tag_by_id(
        tag_id: int,
        user: User = Depends(check_token),
        session: AsyncSession = Depends(Connection.get_session),
):
    tag_service = TagService(TagRepository(session))
    tag = await tag_service.get_tag_by_id(tag_id)

    return tag


@router.get(
    "/notes/{tag_id}",
    summary="Get notes tag by its id",
    description="This endpoint return a tag's notes if available inside the database",
    response_description="The returned data is the requested tag's notes",
    responses={
        200: {"description": "The notes requested returned successfully"},
        404: {"description": "No notes found"},
    },
    status_code=status.HTTP_200_OK,
)
async def get_tags_notes(
        tag_id: int,
        user: User = Depends(check_token),
        session: AsyncSession = Depends(Connection.get_session),
):
    tag_service = TagService(TagRepository(session))
    notes = tag_service.get_tag_notes(tag_id)
    return notes


@router.post(
    "/",
    summary="Create new tag",
    description="This endpoint creates new tag",
    response_description="The returned data is the created tag",
    responses={
        201: {"description": "The tag created successfully"},
        409: {"description": "The tag already exits"},
    },
    status_code=status.HTTP_201_CREATED,
)
async def create_tag(
        tag: TagIn,
        user: User = Depends(check_token),
        session: AsyncSession = Depends(Connection.get_session),
):
    try:
        tag_service = TagService(TagRepository(session))
        tag = await tag_service.create_tag(tag)
        return tag
    except Exception as e:
        await session.rollback()
        raise e


@router.patch(
    "/{tag_id}",
    summary="Rename tag",
    description="This endpoint changes the name of a certain tag by its id",
    response_model=TagOut,
    response_description="The returned data is the updated tag",
    responses={
        200: {"description": "The tag successfully renamed"},
        404: {"description": "Tag not found"},
    },
    status_code=status.HTTP_200_OK,
)
async def rename_folder(
        tag_id: int,
        new_name: str,
        user: User = Depends(check_token),
        session: AsyncSession = Depends(Connection.get_session),
):
    try:
        tag_service = TagService(TagRepository(session))
        tag = await tag_service.rename_tag(tag_id, new_name)
        return tag
    except Exception as e:
        await session.rollback()
        raise e


@router.delete(
    "/{tag_id}",
    summary="Delete a tag",
    description="This endpoint deletes a tag by its id",
    responses={
        200: {"description": "The tag deleted successfully"},
        404: {"description": "Tag not found"},
    },
    status_code=status.HTTP_200_OK,
)
async def delete_tag(
        tag_id: int,
        user: User = Depends(check_token),
        session: AsyncSession = Depends(Connection.get_session),
):
    try:
        tag_service = TagService(TagRepository(session))
        deleted = await tag_service.delete_tag(tag_id)
        return deleted
    except Exception as e:
        await session.rollback()
        raise e
