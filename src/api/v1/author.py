import datetime
import logging

from fastapi import APIRouter, HTTPException, status, Query
from typing import Annotated

from src.models.models import AuthorInsert
from src.db.queries.orm import SyncORMInsert


router = APIRouter()

@router.post('/add', summary='Add author')
async def add_author(
    surname: Annotated[str, Query(description ="Фамилия",max_length=256)],
    firstname: Annotated[str, Query(max_length=256)],
    patronymic: Annotated[str | None, Query(max_length=256)] = None,
    country: Annotated[str | None, Query()] = None,
    birthday: Annotated[datetime.date | None, Query(example='1900-01-01')] = None,
):
    try:
        author = AuthorInsert(
            surname = surname,
            first_name = firstname,
            patronymic = patronymic,
            country = country,
            birthday = birthday
        )
        res = SyncORMInsert.insert_author(**author.dict())
        res['status'] = status.HTTP_201_CREATED
        return res
    except Exception as error:
        logging.error(error)
        raise HTTPException(status_code=400, detail= 'error')
