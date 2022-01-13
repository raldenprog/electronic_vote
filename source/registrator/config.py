import os
from datetime import datetime, timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = '123jp2j1!@E@!ejdasdqo34#$'
    DEBUG = False
    HOST = '0.0.0.0'
    PORT = 13451
    START_VOTING = datetime.now() + timedelta(hours=1)
    START_ACCEPTING_VOTE = datetime.now() + timedelta(hours=2)
    STOP_VOTING = datetime.now() + timedelta(hours=3)
