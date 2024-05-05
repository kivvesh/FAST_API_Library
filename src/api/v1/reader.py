from fastapi import APIRouter, Query, status, HTTPException
from typing import Annotated

from src.db.queries.orm import SyncORMInsert
from src.models.models import ReaderInsert

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