from fastapi import APIRouter

router = APIRouter()


@router.get('/')
async def get_all_notes():
    pass


@router.get('/{folder_id}')
async def get_note_by_id(folder_id: int):
    pass


@router.get('/notes/{folder_id}')
async def get_folders_notes(folder_id: int):
    pass


@router.post('/')
async def create_folder():
    pass


@router.patch('/{folder_id}')
async def rename_folder(folder_id: int):
    pass


@router.delete('/{folder_id}')
async def delete_folder(folder_id: int):
    pass
