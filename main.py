import logging
import uuid

from fastapi import FastAPI, Query, Path, Body, Cookie, Header, Response, status, Form, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder
from enum import Enum
from pydantic import BaseModel, Field, ValidationError
from typing import Annotated, List, Any
import datetime

from uuid import UUID
from bd.queries.orm import SyncORMCreateTables, SyncORMInsert
from models.models import (ReaderInsert, GenreInsert,
                           AuthorInsert, PublishPlaceInsert,
                           BookInsert)


app = FastAPI(

)

@app.post('/create_table')
async def create_table(

):
    try:
        SyncORMCreateTables.create_tables()
        return {'status': 200}
    except:
        raise HTTPException(status_code=400,detail='error')

@app.post('/reader/add', summary='Add reader')
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

@app.post('/genre/add', summary='Add genre')
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

@app.post('/author/add', summary='Add author')
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

@app.post('/publish-place/add', summary='Add publish place')
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

@app.post('/book/add',summary='Add book')
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

