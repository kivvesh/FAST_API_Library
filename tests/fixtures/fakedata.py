import pprint

from faker import Faker

fake = Faker("ru_RU")

class FakeData:
    @staticmethod
    def fake_reader():
        reader = {
            'surname': fake.last_name(),
            'firstname': fake.first_name(),
            'patronymic': f'{fake.first_name()}ивич',
            'phone_number': fake.phone_number(),
            'adress': fake.address()
        }
        return reader
