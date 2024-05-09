import datetime
import uuid

from pydantic import BaseModel, Field

from uuid import UUID

class Message(BaseModel):
    message: str

class IdUUIDMixen(BaseModel):
    id: int
    uuid_id: UUID

class CreateUpdateMixin(BaseModel):
    create_at: datetime.datetime
    update_at: datetime.datetime

class PersonMixin(BaseModel):
    surname: str = Field(max_length=256)
    first_name: str = Field(max_length=256)
    patronymic: str | None = Field(None, max_length=256)

class ReaderInsert(PersonMixin):
    phone_number: str
    address: str | None

class GenreInsert(BaseModel):
    title: str = Field(max_length=256)
    description: str | None

class AuthorInsert(PersonMixin):
    country: str = Field(max_length=256)
    birthday: datetime.date | None

class PublishPlaceInsert(BaseModel):
    title: str = Field(max_length=256)
    city: str

class BookInsert(BaseModel):
    title: str = Field(max_length=256)
    description: str | None
    count_pages: int
    year_publish: datetime.date
    author_id: int | None
    genre_id: int | None
    publish_place_id: int | None

class BookSelect(CreateUpdateMixin,BookInsert,IdUUIDMixen):
    is_book: bool

class BookJoin(BaseModel):
    uuid_id: uuid.UUID
    title: str
    description: str
    count_pages: int
    date_publish: datetime.date
    author: str
    genre: str
    publesh_place: str

    @classmethod
    def from_list(cls, tpl):
        return cls(**{k: v for k,v in zip(cls.__fields__.keys(),tpl)})

class GenreSelect(CreateUpdateMixin,GenreInsert,IdUUIDMixen):
    pass

class AuthorSelect(CreateUpdateMixin, AuthorInsert, IdUUIDMixen):
    pass

class PublishPlaceSelect(CreateUpdateMixin, PublishPlaceInsert, IdUUIDMixen):
    pass

class ReaderSelect(CreateUpdateMixin, ReaderInsert, IdUUIDMixen):
    pass
