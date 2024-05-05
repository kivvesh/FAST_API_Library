import datetime
import logging
from fastapi import APIRouter, HTTPException, status, Query
from typing import Annotated

from src.models.models import BookInsert
from src.db.queries.orm import SyncORMInsert


router = APIRouter()
@router.post('/add',summary='Add book')
async def add_book(
        title: Annotated[str, Query(description='Название книги')],
        count_pages: Annotated[int, Query(description='Количество страниц')],
        year_publish: Annotated[datetime.date, Query()],
        publish_place_id: Annotated[int, Query()] = None,
        author_id: Annotated[int, Query()] = None,
        genre_id: Annotated[int, Query()] = None,
        description: Annotated[str | None, Query()] = None,
):
    try:
        book = BookInsert(
            title = title,
            description = description,
            count_pages = count_pages,
            year_publish = year_publish,
            author_id = author_id,
            genre_id = genre_id,
            publish_place_id = publish_place_id,
        )
        res = SyncORMInsert.insert_book(**book.dict())
        return res
    except Exception as error:
        logging.error(error)
        raise HTTPException(status_code=400,detail='error')