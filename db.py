from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, MetaData, UUID
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, mapper,declarative_base

import psycopg2

Base = declarative_base()

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    full_name = Column(String(300))

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(Integer,ForeignKey('authors.id'))

    author = relationship('Author',back_populates='books')



postgresql_url = 'postgresql://admin:123qwe@localhost:5433/library_database'

engine = create_engine(postgresql_url)

Base.metadata.create_all(engine)

metadata = MetaData()

# if not metadata.tables.get('authors'):
#     table = Table('authors',metadata,
#                   Column('id',Integer,primary_key=True),
#                   Column('full_name',String(300)))
#
# if not metadata.tables.get('books'):
#     table = Table('books',metadata,
#                   Column('id',Integer, primary_key=True),
#                   Column('title',String(200)),
#                   Column('author_id',None,ForeignKey('books.id')))




Session = sessionmaker(bind=engine)



session = Session()

metadata.create_all(engine)


