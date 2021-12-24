import uuid
import hashlib
from auth.db import select_one, insert

DEFAULT_SALT = 'b6c7130abc3e431b9d0df698d1eea4d5'  # Вторая соль, не хранящаяся в бд одинаковая для всех паролей


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
    else:
        raise Exception('Неверный логин или пароль')


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

