from fastapi import APIRouter, Query, HTTPException, status, Path
from typing import Annotated

from db.queries.orm import SyncORMInsert, SyncORMSelect
from models.models import PublishPlaceInsert, PublishPlaceSelect, Message


router = APIRouter()

@router.post('/add', summary='Add publish place')
async def add_publish_place(
        title: Annotated[str, Query(max_length=256)],
        city: Annotated[str, Query(max_length=256)]
):
    try:
        publish_place = PublishPlaceInsert(
            title = title,
            city = city
        )
        res = SyncORMInsert.insert_publish_place(**publish_place.dict())
        res['status'] = status.HTTP_201_CREATED
        return res
    except Exception as error:
        raise HTTPException(status_code=400, detail= 'error')

@router.get(
    '/id/{id}',
    summary='Get publish place by id',
    response_model = PublishPlaceSelect | Message
)
async  def get_publish_place_id(
        id: Annotated[int, Path()]
):
    res = SyncORMSelect.select_publish_place_by_id(id = id)
    if res:
        publish_place = PublishPlaceSelect(**res.__dict__)
        return publish_place
    return Message(message = f'Издательство с id {id} не найдено')