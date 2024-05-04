
from sqlalchemy import insert, select, update
from bd.database import sync_engine, async_engine
from bd.models import metadata_obj, book_table


class SyncCORE:
    @staticmethod
    def create_tables():
        sync_engine.echo = True
        metadata_obj.drop_all(sync_engine)
        metadata_obj.create_all(sync_engine)
        sync_engine.echo = True

    @staticmethod
    def insert_data():
        with sync_engine.connect() as conn:
            # stmt = """
            # INSERT INTO books (id,title) VALUES
            # ('22955e14-0785-4560-bbae-31c30c2812c6','Дюймовочка'),
            # ('5eae8aec-1f86-49d4-a2c0-8d5b3b62f491','Маленький принц');
            # """
            stmt = insert(book_table).values(
                [
                    {'title': 'Дюймовочка'}
                ]
            )

            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def select_books():
        with sync_engine.connect() as conn:
            query = select(book_table)
            result = conn.execute(query)
            books = result.all()
            print(books)

    @staticmethod
    def update_books(title: str = 'Дюймовочка', new_title: str = 'SmallGirl'):
        with sync_engine.connect() as conn:
            # stmt = text('UPDATE books SET title = :new_title where title = :title')#синтаксис :title позволяет через bindparams указывать аргументы
            # stmt = stmt.bindparams(new_title = new_title, title = title)
            stmt = (
                update(book_table)
                .values(title = new_title)
                .filter_by(title = title)
            )


            conn.execute(stmt)
            conn.commit()




class AsyncCORE:

    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_syn(metadata_obj.drop_all())
            await conn.run_syn(metadata_obj.create_all())





