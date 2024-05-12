import datetime
import logging
from fastapi import APIRouter, HTTPException, status, Query, Path, Body
from typing import Annotated

from src.models.models import BookInsert, BookSelect, Message, BookJoin
from src.db.queries.orm import SyncORMInsert, SyncORMSelect, SyncORMUpdate


router = APIRouter()
@router.post(
    '/add',
    summary='Add book',
    # response_model = BookInsert
)
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

@router.get(
    '/id_{id}',
    tags=['book'],
    response_model=BookSelect | Message
)
async def get_book_by_id(
        id: Annotated[int, Path()]
):
    res = SyncORMSelect.select_book(id)
    if res:
        book = BookSelect(**res.__dict__)
        return book
    message = Message(message = f'Книга с id {id} не найдена')
    return message

@router.get(
    '/title_{title}',
    tags=['book'],
    response_model= list[BookSelect] | Message
)
async def get_book_by_title(
        title: Annotated[str, Path()]
):
    res = SyncORMSelect.select_book_by_title(title)

    if res:
        books = [BookSelect(**book[0].__dict__) for book in res]
        return books
    message = Message(message = f'Книга с title {title} не найдена')
    return message

@router.get(
    '/join/{id}',
    tags = ['book'],
    response_model = BookJoin | Message
)
async def join_book(
    id: Annotated[int, Path()]
):
    res = SyncORMSelect.join_book_by_author_and_genre(id = id)
    if res:
        book = BookJoin.from_list(res[0])
        return book
    message = Message(message = f'Книга с id {id} не найдена')
    return message

@router.put(
    '/update/{id}',
    summary = 'Update book by id',
    response_model =  Message
)
async def update_book(
        id: Annotated[int, Path(description='Id book')],
        book: Annotated[BookInsert, Body()]
):
    try:
        SyncORMUpdate.update_book(book_id=id,**book.dict())
        return Message(message = f'Книга с id {id} обновилась')
    except:
        return Message(message = f'Книга с id {id} не обновилась')
