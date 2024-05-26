import logging

import pytest
import json
import os
import shutil
import requests
import time


from FAST_API_Library.tests.fixtures.fakedata import FakeData


@pytest.fixture(autouse=True)
def footer_function_scope():
    """Сообщает продолжительность теста после каждой функции."""
    start = time.time()
    yield
    stop = time.time()
    delta = stop - start
    print('\ntest duration : {:0.3} seconds'.format(delta))

@pytest.fixture(name = 'create_readers', scope = 'session')
def create_readers(tmp_path_factory):
    path_dir = tmp_path_factory.mktemp('fakedata')
    try:
        # if os.path.isdir('fakedata'):
        #     shutil.rmtree('fakedata')
        # os.mkdir('fakedata')
        number_fake_readers = 10
        with open(f'{path_dir}/readers.json','w',encoding='utf8') as file:
            for i in range(number_fake_readers):
                fake_reader = FakeData.fake_reader()
                req = requests.post('http://127.0.0.1:8000/api/v1/reader/add',params=fake_reader)
                file.write(f'{fake_reader}\n')
        return (True,path_dir)
    except Exception as error:
        logging.error(error)
    return False

@pytest.fixture(name = 'get_reader')
def get_fake_readers(create_readers):
    print(create_readers[1],create_readers[0])
    with open(f'{create_readers[1]}/readers.json', 'r', encoding='utf8') as file:
        readers = file.read().split('\n')
    list_readers = []
    for index, reader in enumerate(readers[:-1]):
        dict_reader = eval(reader.replace('\'','"'))
        list_readers.append(dict_reader)
    return list_readers




