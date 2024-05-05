from typing import Annotated

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine, String
from src.db.config import settings

#подключение к бд

sync_engine = create_engine(
    url = settings.DATABASE_URL_psycopg,#url бд
    echo = False, #логирование всех запросов
    pool_size = 5,#размер подключений к бд
    max_overflow = 10#дополнительные подключения
)

async_engine = create_async_engine(
    url = settings.DATABASE_URL_asyncpg,#url бд
    echo = True, #логирование всех запросов
    pool_size = 5,#размер подключений к бд
    max_overflow = 10#дополнительные подключения
)

session_factory = sessionmaker(sync_engine)
async_session_factory = async_sessionmaker(async_engine)

# with Session(sync_engine) as session: #сессия для транзакции
#     session.execute()

str_256 = Annotated[str, 256]

class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)
    }

    def __repr__(self):
        cols = []

        for col in list(self.__table__.columns.keys())[:3]:
            cols.append(f"{col}={getattr(self,col)}")
        return f"<{self.__class__.__name__} {', '.join(cols)}>"


