from main import app
from db import insert, select_one
from Crypto.PublicKey import RSA


PRIVATE_KEY = RSA.generate(2048)
PUBLIC_KEY = PRIVATE_KEY.publickey()


def insert_public_key_user(id_user: int, public_key: str):
    insert(f"""
    insert into public_key (id, key) values ('{id_user}', '{public_key}')
    """)


def get_public_key_user(id_user: int):
    return select_one(f"""
    select key from public_key where id = '{id_user}' 
    """)[0]


@app.route('/')
def index():
    return 'OK'
