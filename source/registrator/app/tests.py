from unittest import TestCase
from app.users.processor import Processor
from pprint import pprint


class Tests(TestCase):

    def test_dev(self):
        Processor().login({
            'id': '1',
            'avatar': 'https://avatars.githubusercontent.com/u/23695322?s=400&v=4',
            'description': 'asdaasdsd',
            'name': 'name',
            'lastname': 'lastname',
            'avatarThumb': 'avatarThumb',
            'phone': 'phone',
            'latitude': 123.123,
            'longitude': 123.123,
        })

    def test_dev_2(self):
        five = Processor().get_next_user({
            'id': 'null'
        })
        test = Processor().swipe({
            'id': 'null',
            'id_second': five[0].get('id'),
            'status': True
        })

    def test_dev_3(self):
        pprint(Processor().get_meeting({
            'id': '4',
        }))
