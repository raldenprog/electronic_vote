import os
import uuid
import hashlib
from validator.db import insert, select


from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256


def sign(encrypted_2_message, private):
    hash_encrypted_2_message = SHA256.new(encrypted_2_message)

    signature = pkcs1_15.new(private).sign(hash_encrypted_2_message)
    return signature


def check_sign(encrypted_2_message, public_key, sign):
    """Проверка подписи от пользоваетеля регистратором"""
    hash_encrypted_message = SHA256.new(encrypted_2_message)
    try:
        pkcs1_15.new(public_key).verify(hash_encrypted_message, sign)
    except:
        return False
    return True


def insert_message(id_user: int, message: str) -> None:
    sql = f"""
      insert into "bulletins"
  (message, id_user)
  values( 
    '{message}', {id_user}
  )
    """
    return insert(sql)


def update_private(id_user: int, private) -> None:
    sql = f"""
      update "bulletins" set private_key = '{private}' where id_user = {id_user}
    """
    return insert(sql)
