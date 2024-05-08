import datetime
import logging

from fastapi import APIRouter, HTTPException, status, Query, Path
from typing import Annotated

from src.models.models import AuthorInsert, AuthorSelect, Message
from src.db.queries.orm import SyncORMInsert, SyncORMSelect


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

@router.get(
    '/{id}',
    summary = 'Get author by id',
    response_model = AuthorSelect | Message
)
async def get_author_by_id(
        id: Annotated[int, Path()]
):
    res = SyncORMSelect.select_author_id(id = id)
    if res:
        return AuthorSelect(**res.__dict__)
    return Message(message=f'Автор с id {id} не найден')
