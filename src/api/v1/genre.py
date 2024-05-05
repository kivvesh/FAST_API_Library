from fastapi import APIRouter, HTTPException, Query, status
from typing import Annotated

from src.models.models import GenreInsert
from src.db.queries.orm import SyncORMInsert

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