from fastapi import APIRouter, Depends, Response, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.tokens import check_token
from src.common.db.connection import Connection
from src.common.utils.generate_etag import generate_etag
from src.models.user import User
from src.repositories.folder_repository import FolderRepository
from src.schemas.folder_schema import FolderOut
from src.services.folder_service import FolderService

router = APIRouter()


@router.get("/")
async def get_all_folders(user: User = Depends(check_token), session: AsyncSession = Depends(Connection.get_session)):
    folder_service = FolderService(FolderRepository(session))
    notes = await folder_service.get_all_folders()
    return notes


@router.get("/{folder_id}",
            summary="Get folder by its id",
            description="This endpoint return a folder if available inside the database",
            response_model=FolderOut,
            response_description="The returned data is the requested folder",
            responses={
                200: {"description": "The folder requested returned successfully"},
                304: {"description": "Folder not modified"},
                404: {"description": "Folder not found"},
            },
            status_code=status.HTTP_200_OK, )
async def get_folder_by_id(folder_id: int,
                           response: Response,
                           if_none_match: str | None = Header(default=None),
                           user: User = Depends(check_token),
                           session: AsyncSession = Depends(Connection.get_session), ):
    folder_service = FolderService(FolderRepository(session))
    folder = await folder_service.get_folder_by_id(folder_id)
    etag = generate_etag(folder.name)
    response.headers["ETag"] = etag

    if etag == if_none_match:
        raise HTTPException(status_code=304, detail="Not modified")

    return folder


@router.get("/notes/{folder_id}")
async def get_folders_notes(folder_id: int):
    pass


@router.post("/")
async def create_folder():
    pass


@router.patch("/{folder_id}")
async def rename_folder(folder_id: int):
    pass


@router.delete("/{folder_id}")
async def delete_folder(folder_id: int):
    pass
