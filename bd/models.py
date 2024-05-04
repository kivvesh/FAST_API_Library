import datetime
import uuid

from typing import Annotated, Optional, List, Union
from sqlalchemy import (Table, Column, Integer, String, MetaData
                        ,ForeignKey, text, DateTime, CheckConstraint, Index, Date, Boolean)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from bd.database import Base, str_256
import enum

from uuid import UUID

metadata_obj = MetaData()

idpk = Annotated[int, mapped_column(primary_key = True)]
uuidpk = Annotated[UUID, mapped_column( server_default = text('gen_random_uuid()'))]
created_at = Annotated[datetime.datetime, mapped_column(server_default = text("TIMEZONE('utc',now())"))]
update_at = Annotated[datetime.datetime, mapped_column(server_default = text("TIMEZONE('utc',now())"),
                                                       onupdate = datetime.datetime.utcnow())]

class Century(enum.Enum):
    century_19 = '19 век'
    century_20 = '20 век'
    century_21 = '21 век'


books_readers_association = Table(
    'books_readers',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id')),
    Column('reader_id',Integer, ForeignKey('readers.id')),
    Column('date_give', DateTime, server_default = text("TIMEZONE('utc',now())")),
    Column('date_take', DateTime, nullable = True, default = None)
)

class ReadersOrm(Base):
    __tablename__ = 'readers'

    id: Mapped[idpk]
    uuid_id: Mapped[uuidpk]
    surname: Mapped[str_256]
    first_name: Mapped[str_256]
    patronymic: Mapped[str_256 | None]
    phone_number: Mapped[str] = mapped_column(unique=True)
    address: Mapped[str | None]
    create_at: Mapped[created_at]
    update_at = Mapped[update_at]

    books: Mapped[Union[List['BooksOrm'], None]] = relationship(
        secondary=books_readers_association
    )


class BooksOrm(Base): #дикларативный стиль
    __tablename__ = 'books'

    id: Mapped[idpk]
    uuid_id: Mapped[uuidpk]
    title: Mapped[str_256]
    description: Mapped[str | None]
    count_pages: Mapped[int]
    year_publish: Mapped[datetime.date | None]
    create_at: Mapped[created_at]
    update_at: Mapped[update_at]
    is_book: Mapped[bool] = mapped_column(default=True, nullable=False)
    author_id: Mapped[int | None] = mapped_column(ForeignKey('authors.id',ondelete = 'CASCADE'))
    genre_id: Mapped[int | None] = mapped_column(ForeignKey('genres.id', ondelete = 'CASCADE'))
    publish_place_id: Mapped[int | None] = mapped_column(ForeignKey('publish_place.id', ondelete='CASCADE'))


    author: Mapped['AuthorOrm'] = relationship(
        back_populates = 'books'
    )
    genre: Mapped['GenreOrm'] = relationship(
        back_populates = 'books'
    )
    publish_place: Mapped['PublishPlaceOrm'] = relationship(
        back_populates = 'books'
    )
    # readers: Mapped[Union[List['ReadersOrm'], None]] = relationship(
    #     secondary=books_readers_association
    # )

    __table_args__ = (
        Index('id_index','id'),
        CheckConstraint("count_pages > 0", name = 'check_positive_count_pages ')
    )


class PublishPlaceOrm(Base):
    __tablename__ = 'publish_place'

    id: Mapped[idpk]
    uuid_id: Mapped[uuidpk]
    title: Mapped[str] = mapped_column(unique=True)
    city: Mapped[str]
    create_at: Mapped[created_at]
    update_at = Mapped[update_at]

    books: Mapped[list['BooksOrm']] = relationship(
        back_populates = 'publish_place'
    )


class AuthorOrm(Base):
    __tablename__ = 'authors'

    id: Mapped[idpk]
    uuid_id: Mapped[uuidpk]
    surname: Mapped[str_256]
    first_name: Mapped[str_256]
    patronymic: Mapped[str_256 | None]
    country: Mapped[str | None] #= mapped_column(nullable=True)
    birthday: Mapped[datetime.date | None]
    create_at: Mapped[created_at]
    update_at: Mapped[update_at]

    books: Mapped[list['BooksOrm']] = relationship(
        back_populates = 'author'
    )


class GenreOrm(Base):
    __tablename__ = 'genres'

    id: Mapped[idpk]
    uuid_id: Mapped[uuidpk]
    title: Mapped[str_256] = mapped_column(unique=True)
    description: Mapped[str | None]
    create_at: Mapped[created_at]
    update_at = Mapped[update_at]

    books: Mapped[list['BooksOrm']] = relationship(
        back_populates = 'genre'
    )

from sqlalchemy import UUID

book_table = Table( #императивный стиль
    'books',
    metadata_obj,
    Column('id', UUID, primary_key=True,server_default = text('gen_random_uuid()')),
    Column('title',String),
    Column('create_at',DateTime,server_default = text("TIMEZONE('utc',now())")),
    Column('update_at',DateTime,server_default = text("TIMEZONE('utc',now())"),
                                                       onupdate = datetime.datetime.utcnow())
)







