from db import, select, select_old
from Crypto.Hash import SHA256
import hashlib

def check():
    sql = '''
select * from bulletins
    '''
    result_sql = select(sql)
    result_sql_old = select_old(sql)

    for row in result_sql_old:
        id_bulletin = row['id']
        old_message = row['message']
        new_message = result_sql[id_bulletin]
        if not new_message:
            raise Exception('Бюллетень не найден')

        hash_old = hashlib.sha256(old_message.encode()).hexdigest()
        hash_new = hashlib.sha256(new_message.encode()).hexdigest()

        if hash_old != hash_new:
            raise Exception('Бюллетени не совпадают')