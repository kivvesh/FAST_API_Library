import json
import logging

import pytest
import psycopg2
import requests

from FAST_API_Library.src.db.config import settings

def test_fake_connect_db():
    try:
        with pytest.raises(psycopg2.OperationalError) as error:

            connection = psycopg2.connect(
                user = settings.POSTGRES_USER,
                password = settings.POSTGRES_PASSWORD,
                host = settings.POSTGRES_HOST,
                port = '120.0.0.1',
                database = settings.POSTGRES_DB
            )
            logging.error(error)
    except:
        raise Exception('Подключение не состоялось')


# @pytest.mark.smoke
def test_connect_db():
    try:
        connection = psycopg2.connect(
            user = settings.POSTGRES_USER,
            password = settings.POSTGRES_PASSWORD,
            host = settings.POSTGRES_HOST,
            port = settings.POSTGRES_PORT,
            database = settings.POSTGRES_DB
        )
    except:
        raise Exception('Подключение не состоялось')

# @pytest.mark.smoke
def test_create_tables():
    req = requests.post('http://127.0.0.1:8000/create_tables')
    assert req.status_code == 200

def test_add_reader(create_readers):
    assert create_readers[0] == True

# @pytest.mark.parametrize(
#     'readers',
#     get_reader()
# )
def test_get_readers(get_reader):
    for index, value in enumerate(get_reader):
        req = requests.get(f'http://127.0.0.1:8000/api/v1/reader/id/{index+1}')
        assert value['firstname'] == req.json()['first_name']
        assert value['surname'] == req.json()['surname']

# readers = (
#     [1,4,9],
#     [64,49]
# )
#
# @pytest.mark.parametrize(
#     'qwrt',
#     readers
# )
# def test_test(qwrt):
#     for i in qwrt:
#         assert i % 1 == 0
