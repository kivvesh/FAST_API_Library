import datetime

from pydantic import BaseModel, Field

from uuid import UUID

class IdUUIDMixen(BaseModel):
    id: int
    uuid_id: UUID

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

