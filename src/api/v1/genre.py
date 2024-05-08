from fastapi import APIRouter, HTTPException, Query, status, Path
from typing import Annotated

from src.models.models import GenreInsert, GenreSelect, Message
from src.db.queries.orm import SyncORMInsert, SyncORMSelect

router = APIRouter()


@router.post('/add', summary='Add genre')
async def insert_genre(
    title: Annotated[str, Query(max_length=256)],
    description: Annotated[str | None, Query()] = None
):
    try:
        genre = GenreInsert(
            title = title,
            description = description
        )
        res = SyncORMInsert.insert_genre(**genre.dict())
        res['status'] = status.HTTP_201_CREATED
        return  res
    except Exception as error:
        # logging.error(error)
        raise HTTPException(status_code=400, detail= 'error')

@router.get(
    '/{id}',
    summary = 'Get genre by id',
    response_model = GenreSelect | Message
)
async def get_genre_by_id(
        id: Annotated[int, Path()]
):
    res = SyncORMSelect.select_genre_id(id = id)
    if res:
        return GenreSelect(**res.__dict__)
    return Message(message = f'Жанр с id {id} не найден')
