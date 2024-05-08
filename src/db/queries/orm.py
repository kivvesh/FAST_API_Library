import datetime

from sqlalchemy import select, update, insert
from sqlalchemy.orm import aliased, joinedload, selectinload
from src.db.database import sync_engine, async_engine, session_factory, async_session_factory, Base
from src.db.models import (metadata_obj, BooksOrm, AuthorOrm, GenreOrm, ReadersOrm
, books_readers_association, PublishPlaceOrm)


class SyncORMCreateTables:
    @staticmethod
    def create_tables():
        # sync_engine.echo = False
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)
        # sync_engine.echo = True

class SyncORMInsert:
    @staticmethod
    def insert_author(
            surname: str,
            first_name=str,
            patronymic: str | None = None,
            country: str | None = None,
            birthday: datetime.date | None = None,
    ):
        author = AuthorOrm(
            surname=surname,
            first_name=first_name,
            patronymic=patronymic,
            birthday=birthday,
            country=country
        )
        with session_factory() as session:
            session.add(author)
            session.commit()
        res = {'result': f'Автор создан'}
        return res

    @staticmethod
    def insert_genre(
        title: str,
        description: str | None = None
    ):
        genre = GenreOrm(title=title,description = description)
        with session_factory() as session:
            session.add_all([genre])
            session.commit()
            return {'result': f'Жанр {title} создан'}


    @staticmethod
    def insert_reader(
            surname: str,
            first_name: str,
            phone_number = str,
            patronymic: str | None = None,
            address: str | None = None
    ):
        reader = ReadersOrm(
            surname=surname,
            first_name=first_name,
            patronymic=patronymic,
            phone_number = phone_number,
            address = address
        )
        with session_factory() as session:
            session.add(reader)
            session.commit()
            return {'result': f'Читатель {surname} {first_name} создан'}


    @staticmethod
    def insert_publish_place(
            title: str,
            city: str
    ):
        publish_place = PublishPlaceOrm(
            title=title,
            city=city
        )
        with session_factory() as session:
            session.add(publish_place)
            session.commit()
        res = {'result': f"Издательство {title} создано"}
        return res

    @staticmethod
    def insert_book(
        title: str,
        count_pages: int,
        description: str | None = None,
        year_publish: datetime.date | None = None,
        author_id: int | None = None,
        genre_id: int | None = None,
        publish_place_id: int | None = None,
    ):
        # with session_factory() as session:
        #     author = session.query(AuthorOrm).filter(AuthorOrm.id == author_id).scalar()


        book = BooksOrm(
            title=title,
            count_pages = count_pages,
            description = description,
            year_publish = year_publish,
            author_id = author_id,
            genre_id = genre_id,
            publish_place_id = publish_place_id
        )
        with session_factory() as session:
            session.add_all([book])
            session.flush()#команда для отправки данных в субд
            session.commit()
        res = {'result': f'Книга {title} добавлена'}
        return res

    @staticmethod
    def insert_book_reader(
            book_id: int,
            reader_id: int
    ):
        with session_factory() as session:
            # query = select(BooksOrm).filter(BooksOrm.id == book_id)
            # book = session.execute(query).scalar()
            # book.is_book = False
            #
            # query = select(ReadersOrm).filter(ReadersOrm.id == reader_id)
            # reader = session.execute(query).scalar()
            # reader.books.append(book)

            query = (
                insert(
                    books_readers_association
                )
                .values(reader_id = 1, book_id = 1)
            )
            session.execute(query)

            # query = (
            # select(ReadersOrm)
            # .filter(ReadersOrm.id == reader_id)
            # )
            # reader = session.execute(query).scalar()
            # reader.books.append(book)
            session.commit()

    @staticmethod
    def update_book_reader(
            # book_id: int,
            # reader_id: int
    ):
        b_r = aliased(books_readers_association)
        b = aliased(BooksOrm)
        with session_factory() as session:
            query = (
                update(b_r)
                .where(b_r.c.book_id == 1)
                .values(date_take = datetime.datetime.utcnow())
            )
            session.execute(query)

            query = (
                update(
                    b
                )
                .where(b.id == 1)
                .values(is_book = True)
            )
            session.execute(query)
            session.commit()

class SyncORMUpdeate:
    @staticmethod
    def update_book(
            book_id: int,
            **kwargs
            # title: str,
            # count_pages: int,
            # description: str | None = None,
            # year_publish: datetime.date | None = None,
            # author_id: int | None = None,
            # genre_id: int | None = None,
            # publish_place_id: int | None = None,
    ):
        with session_factory() as session:
            b =  aliased(BooksOrm)
            # query = (
            #     select(b)
            #     .filter(b.id == book_id)
            # )
            # book_id = session.execute(query).scalar()
            #print(kwargs)
            query = (
                update(b)
                .where(b.id == book_id)
                .values(kwargs)
            )
            session.execute(query)
            session.commit()

class SyncORMSelect:
    @staticmethod
    def select_book(
            id: int
    ):
        with session_factory() as session:
            query = (
                select(BooksOrm)
                .filter(BooksOrm.id == id)
            )
            res = session.execute(query).scalar()
        return res

    @staticmethod
    def select_book_by_title(
            title: str
    ):
        with session_factory() as session:
            query = (
                select(BooksOrm)
                .filter(BooksOrm.title.contains(title))
            )
            res = session.execute(query).all()
        return res

    @staticmethod
    def join_book_by_author_and_genre(
            id: int
    ):
        b = aliased(BooksOrm)
        a = aliased(AuthorOrm)
        g = aliased(GenreOrm)
        p = aliased(PublishPlaceOrm)
        with session_factory() as session:
            query = (
                select(
                    b.uuid_id,
                    b.title,
                    b.description,
                    b.count_pages,
                    b.year_publish,
                    a.surname + ' ' + a.first_name + ' ' + a.patronymic,
                    g.title,
                    p.title
                )
                .select_from(b)
                .join(a, a.id == b.author_id)
                .join(g, g.id == b.genre_id)
                .join(p, p.id == b.publish_place_id)
                .filter(b.id == id)
            )
            res = session.execute(query).all()
        return res

    @staticmethod
    def search_books_by_genre(
            genre: str | None = str
    ):
        b = aliased(BooksOrm)
        g = aliased(GenreOrm)
        a = aliased(AuthorOrm)

        with session_factory() as session:
            query = (
                select(
                    b.title,
                    a.surname,
                    g.title
                )
                .select_from(b)
                .join(a, b.author_id == a.id)
                .join(g, g.id == b.genre_id)
                .filter(g.title.contains(genre))
            )
            res = session.execute(query).all()
        return res

    @staticmethod
    def select_genre_id(id):
        g = aliased(GenreOrm)
        with session_factory() as session:
            query = (
                select(g)
                .filter(g.id == id)
            )
            res = session.execute(query).scalar()
            return res

    @staticmethod
    def select_author_id(id):
        a = aliased(AuthorOrm)
        with session_factory() as session:
            query = (
                select(a)
                .filter(a.id == id)
            )
            res = session.execute(query).scalar()
            return res


    @staticmethod
    def select_books():
        with session_factory() as session:
            title_book = 'Small girl'
            query = select(BooksOrm)
            result = session.execute(query)
            books = result.scalars().all() #метод scalars берет первый элемент каждого кортежа списка
            print(books)
            #book_jack = session.get(BooksOrm, {'id':'id'})

    # @staticmethod
    # def select_book_by_title():
    #     with session_factory() as session:
    #         query = (
    #             select(
    #                 BooksOrm.title,
    #                 BooksOrm.count_pages
    #                 #cast(func.avg(BooksOrm.count_pages),Integer).label('avg_pages'),
    #             )
    #             .select_from(BooksOrm)
    #             .filter(and_(
    #                 BooksOrm.title.contains('Small'),
    #                 BooksOrm.count_pages >= 500
    #             ))
    #             # .group_by(BooksOrm.count_pages)
    #             # .having(cast(func.avg(BooksOrm.count_pages),Integer).label('avg_pages') > 300)
    #         )
    #
    #         print(query.compile(compile_kwargs = {'literal_binds':True}))
    #         result = session.execute(query)
    #         res = result.all()
    #         print(res)
    @staticmethod
    def join_book_author():
        '''
        select b.title, a.fullname, avg(b.count_pages) as pages
        from books as b join authors as a on b.author_id = a.id and a.fullname like '%Пуш%'
        order by pages;
        '''
        with session_factory() as session:
            b = aliased(BooksOrm)
            a = aliased(AuthorOrm)

            query = (
                select(
                    b.title,
                    a.fullname
                )
                .select_from(b)
                .join(a, a.id == b.author_id)
                .order_by(a.create_at.desc())
            )
            result = session.execute(query).all()
            title_list = [i.title for i in result]
            print(title_list)

    @staticmethod
    def select_books_with_lazy_raletionship():
        with session_factory() as session:
            query = (
                select(AuthorOrm)
            )
            res = session.execute(query).scalars().all()

            author1 = res[0].books
            print(author1)
            author2 = res[1].books
            print(author2)

    @staticmethod
    def select_books_with_joined_raletionship():
        with session_factory() as session:
            query = (
                select(AuthorOrm)
                .options(joinedload(AuthorOrm.books))
            )
            res = session.execute(query).unique().scalars().all()

            author1 = res[0].books
            print(author1)
            author2 = res[1].books
            print(author2)

    @staticmethod
    def select_books_with_selectin_raletionship():
        with session_factory() as session:
            query = (
                select(AuthorOrm)
                .options(selectinload(AuthorOrm.books))
            )
            res = session.execute(query).unique().scalars().all()

            author1 = res[0].books
            print(author1)
            author2 = res[1].books
            print(author2)



    @staticmethod
    def update_books(title: str = 'Small girl', new_title: str = 'SmallGirl'):
        with session_factory() as session:
            query = session.query(BooksOrm).filter(BooksOrm.title == title).scalar()
            query.title = new_title
            session.expire_all()# отмена всех изменений или expire(obj) - отмена изменений для конкретного объекта
            session.commit()






class AsyncORM:

    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_syn(metadata_obj.drop_all())
            await conn.run_syn(metadata_obj.create_all())

    @staticmethod
    async def async_insert_data():  # ассинхронное добавление записей
        async with async_session_factory() as session:
            book_example1 = BooksOrm(title='Small prince')
            book_example2 = BooksOrm(title='Small girl')
            # session.add(book_example1)
            # session.add(book_example2)s
            session.add_all([book_example1, book_example2])
            await session.commit()
