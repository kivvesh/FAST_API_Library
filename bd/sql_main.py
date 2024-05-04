#from queries.core import SyncCORE, AsyncCORE
import asyncio
import datetime
import uuid

from bd.queries.orm import AsyncORM, SyncORMCreateTables, SyncORMInsert, SyncORMSelect, SyncORMUpdeate

SyncORMCreateTables.create_tables()#создание таблиц по моделям
#добавление автора
SyncORMInsert.insert_author(
    surname = 'Пушкин',
    first_name = 'Александр',
    patronymic = 'Сергеевич',
    birthday = datetime.date(year=1799, month=5, day=26),
    country = 'Российская империя'
)
#добавление жанра
SyncORMInsert.insert_genre(
    title = 'Сказки',
    description = 'Выдуманные истории'
)
#добавление читателя
SyncORMInsert.insert_reader(
    surname='Шевченко',
    first_name='Виктор',
    patronymic='Дмитриевич',
    address = 'Москва',
    phone_number = '799304983928'
)
#добавление издательства
SyncORMInsert.insert_publish_place(
    title = 'ООО ВСЕПечать',
    city = 'Москва'
)
#добавление книги
SyncORMInsert.insert_book(
    title = 'Капитанская дочка',
    count_pages = 120,
    description = 'Повесть',
    year_publish = datetime.date(year = 2010, month=10, day=20),
    author_id=1,
    genre_id=1,
    publish_place_id=1
)
#добавление взятие книги
SyncORMInsert.insert_book_reader(
    book_id = 1,
    reader_id = 1
)
#возвращение книги
SyncORMInsert.update_book_reader(

)


#поиск книги по id
SyncORMSelect.select_book(
    id = 1
)
#поиск книги по title
SyncORMSelect.select_book_by_title(
    title = 'Капитанская'
)
#поиск книги по id
SyncORMSelect.join_book_by_author_and_genre(
    title = 'Капитанская дочка',
    genre = 'Сказки'
)
#поиск книг по жанрам
SyncORMSelect.search_books_by_genre(
    genre = 'Сказки'
)

SyncORMUpdeate.update_book(
    book_id=1,
    title = 'Капитанская дрочка',
    # uuid_id = uuid.uuid4(),
    count_pages = 200,
    description = 'Повесть',
    year_publish = datetime.date(year = 2010, month=10, day=20),
    author_id=1,
    genre_id=1,
    publish_place_id=1
)





# SyncORM.insert_author()
# SyncORM.insert_genre()
# SyncORM.insert_books()
#SyncORM.select_book_by_title()
# SyncORM.join_book_author()
# SyncORM.select_books_with_lazy_raletionship()
# SyncORM.select_books_with_joined_raletionship()
# SyncORM.select_books_with_selectin_raletionship()

# SyncORM.update_books()

# SyncCORE.create_tables()
# SyncCORE.insert_data()
# SyncCORE.select_books()
# SyncCORE.update_books()
# SyncCORE.select_books()

# asyncio.run(AsyncORM.async_insert_data())
