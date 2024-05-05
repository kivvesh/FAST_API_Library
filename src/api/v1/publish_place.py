from fastapi import APIRouter, Query, HTTPException, status
from typing import Annotated

from src.db.queries.orm import SyncORMInsert
from src.models.models import PublishPlaceInsert


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