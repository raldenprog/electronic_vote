from validator.db import insert, select
from Crypto.Hash import SHA256
import hashlib
from Crypto.Signature import pkcs1_15
import requests
from Crypto.PublicKey import RSA


def check_sign(encrypted_2_message, public_key, sign):
    """Проверка подписи от пользоваетеля регистратором"""
    hash_encrypted_message = SHA256.new(encrypted_2_message)
    try:
        pkcs1_15.new(public_key).verify(hash_encrypted_message, sign)
    except:
        return False
    return True

def check():
    sql = '''
select * from bulletins
    '''
    result_sql = select(sql)

    for row in result_sql:
        id_user = row['id_user']
        message_user = row['message']
        sign_user = row['sign_user']
        sign_registrator = row['sign_registrator']
        public_key_user_r = requests.get(f'http://0.0.0.0:13451/public/{id_user}')
        public_key_user = public_key_user_r.content.decode()
        public_key_registrator_r = requests.get(f'http://0.0.0.0:13451/public')
        public_key_registrator = public_key_registrator_r.content.decode()
        checked_user_sign = check_sign(message_user, RSA.importKey(public_key_user), sign_user)
        checked_registrator_sign = check_sign(message_user, RSA.importKey(public_key_registrator), sign_registrator)
        if not checked_user_sign:
            raise Exception('Ошибка в подписи пользователя')
        if not checked_registrator_sign:
            raise Exception('Ошибка в подписи регистратора')
