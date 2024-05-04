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
from models.models import ReaderInsert, GenreInsert, AuthorInsert

SyncORMCreateTables.create_tables()

app = FastAPI(

)

@app.post('/reader/add', summary='Add reader')
async def insert_reader(
        surname: Annotated[str, Query(description ="Фамилия",max_length=256)],
        firstname: Annotated[str, Query(max_length=256)],
        phone_number: Annotated[str, Query(max_length=256)],
        patronymic: Annotated[str | None, Query(max_length=256)] = None,
        address: Annotated[str | None, Query(max_length=256)] = None,
):
    reader = ReaderInsert(
        surname = surname,
        first_name = firstname,
        patronymic = patronymic,
        phone_number = phone_number,
        address = address
    )
    res = SyncORMInsert.insert_reader(**reader.dict())
    return res

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
        status = SyncORMInsert.insert_genre(**genre.dict())
        return  status
    except Exception as error:
        # logging.error(error)
        return {'error': str(error)}

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
        return res
    except Exception as error:
        return {'error': str(error)}
