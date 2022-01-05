import uuid
import hashlib
from validator.db import select_one, insert, select


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
