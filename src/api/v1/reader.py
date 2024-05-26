from fastapi import APIRouter, Query, status, HTTPException, Path
from typing import Annotated

from db.queries.orm import SyncORMInsert, SyncORMSelect
from models.models import ReaderInsert, ReaderSelect, Message

router = APIRouter()

@router.post('/add', summary='Add reader')
async def insert_reader(
        surname: Annotated[str, Query(description ="Фамилия",max_length=256)],
        firstname: Annotated[str, Query(max_length=256)],
        phone_number: Annotated[str, Query(max_length=256)],
        patronymic: Annotated[str | None, Query(max_length=256)] = None,
        address: Annotated[str | None, Query(max_length=256)] = None,
):
    try:
        reader = ReaderInsert(
            surname = surname,
            first_name = firstname,
            patronymic = patronymic,
            phone_number = phone_number,
            address = address
        )
        res = SyncORMInsert.insert_reader(**reader.dict())
        res['status'] = status.HTTP_201_CREATED
        return res
    except Exception as error:
        raise HTTPException(status_code=400, detail= 'error')

@router.get(
    '/id/{id}',
    summary='Get reader by id',
    response_model=ReaderSelect | Message
)
async def get_reader_by_id(
        id: Annotated[int, Path()]
):
    res = SyncORMSelect.get_reader_by_id(id = id)
    if res:
        reader = ReaderSelect(**res.__dict__)
        return reader
    return Message(message = f'Читатель с id {id} не найден')
