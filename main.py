import logging

from fastapi import FastAPI, Query, status, HTTPException
from typing import Annotated
import datetime

from src.api.v1 import reader, genre, author, publish_place, book
from src.db.queries.orm import SyncORMCreateTables


app = FastAPI(
    title='APIlibrary',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json'
)

@app.post('/create_tables',tags=['Create tables'])
async def create_table(

):
    try:
        SyncORMCreateTables.create_tables()
        return {'status': 200}
    except:
        raise HTTPException(status_code=400,detail='error')

app.include_router(reader.router,prefix='/api/v1/reader',tags=['reader'])
app.include_router(genre.router,prefix='/api/v1/genre',tags=['genre'])
app.include_router(author.router,prefix='/api/v1/author',tags=['author'])
app.include_router(publish_place.router,prefix='/api/v1/publish-place',tags=['publish-place'])
app.include_router(book.router,prefix='/api/v1/book',tags=['book'])







