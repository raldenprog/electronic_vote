from validator.db import insert, select
from Crypto.Cipher import PKCS1_OAEP


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


def decrypt(encrypt_key, message):
    return PKCS1_OAEP.new(encrypt_key).decrypt(message)


def decrypt_messages():
    sql = f"""
      select * from "bulletins" where private_key is not null
    """
    result_sql = select(sql)
    results = {}
    for row in result_sql:
        decrypted = decrypt(row['messsage'], row['private_key'])
        count = results.get(decrypted)
        results[decrypted] = count
    return results

def get_keys():
    sql = """
    select id, private_key from "bulletins" where private_key is not null
    """