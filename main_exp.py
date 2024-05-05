import uuid

from fastapi import FastAPI, Query, Path, Body, Cookie, Header, Response, File, UploadFile, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.encoders import jsonable_encoder
from enum import Enum
from pydantic import BaseModel, Field
from typing import Annotated, Any
import datetime

from uuid import UUID
from queries.orm import SyncORMCreateTables

SyncORMCreateTables.create_tables()



class BookChoice(str,Enum):
    book1 = 'книга1'
    book2 = 'книга12'

class Author(BaseModel):
    full_name: str = Field(title = 'Имя автора',example='Булгаков Михаил Афанасьевич')
    country: str | None = Field(default=None, title='страна')

class Genre(BaseModel):
    title: str = Field(title = 'Название', example = 'Роман')
    description: str | None = Field(title = 'Описание жанра', default=None)

class Book(BaseModel):#Модель для объектов Book
    uuid_book: UUID = uuid.uuid4()
    title: str
    description: str | None = Field(max_length=300, default = None)
    pages: int | None = None
    genres: list[Genre] = Field(title = 'Жанры')
    authors: list[Author] = Field(title = 'Авторы')
    date_created: datetime.datetime = Field(title = 'Дата создания')

    # model_config = {
    #     "json_schema_extra": {
    #         "examples": [
    #             {
    #                 "title": "Название",
    #                 "description": "Описание",
    #                 "pages": 0,
    #                 "genres": [
    #                     {
    #                         "title": "Название жанра",
    #                         "description": "Описание жанра"
    #                     }
    #                 ],
    #                 "authors": [
    #                     {
    #                         "full_name": "Имя автора",
    #                         "country": "Страна рождения автора"
    #                     }
    #                 ]
    #             }
    #         ]
    #     }
    # }

class BookAnswer(Book):
    status: int

app = FastAPI()

@app.get('/books/')
async def books(page: int = 1):
    return {'message': 'Books'}

@app.get('/exception/{name_ex}')
async def exception(
    name_ex: Annotated[ str, Path(title = 'name_path')]
):
    if name_ex:
        raise HTTPException(status_code=404)
    return {'status':'ok'}


def write(name, f):
    with open(f'{name}','w') as file:
        file.write(f)

@app.post('/load-file',deprecated=True)
async def load_file(
        file: Annotated[bytes,File()],
        uploadfile: UploadFile
):
    write(uploadfile.filename,uploadfile.file.read().decode())
    return {'file_size':len(file)}



@app.get('/book/{book_id}')
async def detail_book(book_id:BookChoice):
    return {'id':book_id.name}

@app.get('/redirect')
async def redirect(off: bool = False) -> Response:
    if off:
        return RedirectResponse(url = 'http://127.0.0.1:8000/docs')
    return {'status': 'Off-None'}


def status_500(book: BookAnswer):
    book['status'] = 500
    return book


@app.post(
    '/book',
    #response_model=BookAnswer, - модель ответа
    #response_model_include = {"status"}, - атрибуты модели ответа
    #status_code= status.HTTP_201_CREATED, - статус ответа
    summary = 'Method by create book',
    response_description = "Book created"
)
async def create_book(
        book: Annotated[Book, Body(embed=True, title= 'Book', description='Добавление книги')],
        id_user: Annotated[UUID, Cookie()] = uuid.uuid4(),
        user_agent: Annotated[str | None, Header()] = None,
        x_token: Annotated[list[str] | None, Header()] = None,
) -> Any:
    if not Book.validate(book):
        return {'false':True}
    response = book.dict()
    response.update({'status':200})
    response = status_500(response)
    json_book = jsonable_encoder(book)
    return json_book


@app.put('/book/{book_id}')
async def update_book(
        book_id: Annotated[int, Path(title = 'Id book',gt=0)],
        book: Annotated[Book,Body(embed=True)],
        author: Annotated[str, Query(max_length=100)] = 'kivvesh',
        genres: Annotated[list[str] | None, Query(title = "qwe",description='список жанров')] = None,

):
    result = {'id':book_id,**book.dict()}
    if author and genres:
        result.update({'genres':genres})
    return result


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100,):
    return {'1':'1'}

async def common_parameters2(book: Annotated[Book, Body()], i: str):
    return book.dict()

@app.get('/items/')
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons

book_dict = Annotated[dict, Depends(common_parameters2)]
@app.post('/itemsBook/')
async def read_items(book: book_dict):
    return book


