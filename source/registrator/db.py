import psycopg2
import psycopg2.extras
from pprint import pprint


def connect():
    conn = psycopg2.connect(dbname='registrator', user='raldenprog',
                            password='Nedlar_proG', host='localhost')
    return conn, conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


def select(sql: str):
    pprint(sql)
    conn, cursor = connect()
    cursor.execute(sql)
    return cursor.fetchall()


def select_one(sql: str):
    pprint(sql)
    conn, cursor = connect()
    cursor.execute(sql)
    return cursor.fetchone()


def insert(sql: str):
    pprint(sql)
    conn, cursor = connect()
    cursor.execute(sql)
    conn.commit()
    try:
        return cursor.fetchone()
    except:
        pass
