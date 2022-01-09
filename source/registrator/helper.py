import uuid
import hashlib
from db import select_one, insert, select

DEFAULT_SALT = 'b6c7130abc3e431b9d0df698d1eea4d5'  # Вторая соль, не хранящаяся в бд одинаковая для всех паролей


def save_public_key_user(id_user: int, public_key: str) -> bool:
    exist_key = public_key_by_id(id_user)
    if not exist_key:
        sql = f"""
          insert into "public_keys"
      (id_user, key)
      values( 
        {id_user}
        , '{public_key}'
      )
        """
        insert(sql)
        return True
    else:
        return False


def public_key_by_id(id_user: int):
    sql = f"""
      select key from "public_keys" where id_user = {id_user}::int
    """
    return select_one(sql)


def auth(login: str, password: str):
    """
    Функция авторизации пользователя
    Args:
        login: логин
        password: пароль

    Returns:
        идентификатор пользователя
    """
    user = get_user_by_login(login)
    if user and check_password(user['hash_pass'], password):
        return user


def registration(login: str, password: str) -> int:
    """
    Функция регистрации пользователя
    Args:
        login: логин
        password: пароль

    Returns:
        идентификатор пользователя
    """
    hash_pass = hash_password(password)
    sql = f"""
    insert into auth (login, hash_pass) values ('{login}', '{hash_pass}') returning id
    """
    return insert(sql)['id']


def get_user_by_login(login: str):
    """Получение пользователя по логину"""
    sql_query = f"""
    select * from auth where login = '{login}' 
    """
    return select_one(sql_query)


def get_salt():
    """Метод возвращает соль"""
    return uuid.uuid4().hex


def hash_password(password: str):
    """Функция хеширования пароля"""
    salt = get_salt()
    return hashlib.sha256(DEFAULT_SALT.encode() + salt.encode() + password.encode()).hexdigest() + salt


def check_password(hashed_password, user_password):
    """Проверка пароля и хеша на соответствие"""
    len_salt = len(get_salt())
    password = hashed_password[:-len_salt]
    salt = hashed_password[-len_salt:]
    return password == hashlib.sha256(DEFAULT_SALT.encode() + salt.encode() + user_password.encode()).hexdigest()

