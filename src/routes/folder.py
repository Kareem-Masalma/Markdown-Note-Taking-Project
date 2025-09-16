from fastapi import APIRouter, Depends, status

from src.auth.tokens import check_token
from src.dependencies.folder import get_folder_service
from src.schemas.folder import FolderResponse, FolderRequest
from src.schemas.note import NoteResponse
from src.services.folder import FolderService

router = APIRouter(dependencies=[Depends(check_token)])


@router.get(
    "/",
    summary="Get all folders",
    description="This endpoint return a all folders if available inside the database",
    response_model=list[FolderResponse],
    response_description="The list of folders",
    responses={
        200: {"description": "The folders requested returned successfully"},
        404: {"description": "No folders found"},
    },
    status_code=status.HTTP_200_OK,
)
async def get_all_folders(folder_service: FolderService = Depends(get_folder_service)):
    notes = await folder_service.get_all_folders()
    return notes


@router.get(
    "/{folder_id}",
    summary="Get folder by its id",
    description="This endpoint return a folder if available inside the database",
    response_model=FolderResponse,
    response_description="The returned data is the requested folder",
    responses={
        200: {"description": "The folder requested returned successfully"},
        404: {"description": "Folder not found"},
    },
    status_code=status.HTTP_200_OK,
)
async def get_folder_by_id(
    folder_id: int, folder_service: FolderService = Depends(get_folder_service)
):
    folder = await folder_service.get_folder_by_id(folder_id)

    return folder


@router.get(
    "/notes/{folder_id}",
    summary="Get notes folder by its id",
    description="This endpoint return a folder's notes if available inside the database",
    response_model=list[NoteResponse],
    response_description="The returned data is the requested folder's notes",
    responses={
        200: {"description": "The notes requested returned successfully"},
        404: {"description": "No notes found"},
    },
    status_code=status.HTTP_200_OK,
)
async def get_folders_notes(
    folder_id: int, folder_service: FolderService = Depends(get_folder_service)
):
    notes = await folder_service.get_folder_notes(folder_id)
    return notes


@router.post(
    "/",
    summary="Create new folder",
    description="This endpoint creates new folder",
    response_description="The returned data is the created folder",
    responses={
        201: {"description": "The folder created successfully"},
        409: {"description": "The folder already exits"},
    },
    status_code=status.HTTP_201_CREATED,
)
async def create_folder(
    folder: FolderRequest, folder_service: FolderService = Depends(get_folder_service)
):
    folder = await folder_service.create_folder(folder)
    return folder


@router.patch(
    "/{folder_id}",
    summary="Rename folder",
    description="This endpoint changes the name of a certain folder by its id",
    response_model=FolderResponse,
    response_description="The returned data is the updated folder",
    responses={
        200: {"description": "The folder successfully renamed"},
        404: {"description": "Folder not found"},
    },
    status_code=status.HTTP_200_OK,
)
async def rename_folder(
    folder_id: int,
    new_name: str,
    folder_service: FolderService = Depends(get_folder_service),
):
    folder = await folder_service.rename_folder(folder_id, new_name)
    return folder


@router.delete(
    "/{folder_id}",
    summary="Delete a folder",
    description="This endpoint deletes a folder by its id",
    responses={
        200: {"description": "The folder deleted successfully"},
        404: {"description": "Folder not found"},
    },
    status_code=status.HTTP_200_OK,
)
async def delete_folder(
    folder_id: int, folder_service: FolderService = Depends(get_folder_service)
):
    deleted = await folder_service.delete_folder(folder_id)
    return deleted
