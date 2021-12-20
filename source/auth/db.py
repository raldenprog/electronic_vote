import psycopg2
import psycopg2.extras


def connect():
    conn = psycopg2.connect(dbname='registrator', user='raldenprog',
                            password='Nedlar_proG', host='localhost')
    return conn, conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


def select(sql: str):
    conn, cursor = connect()
    cursor.execute(sql)
    return cursor.fetchall()


def select_one(sql: str):
    conn, cursor = connect()
    cursor.execute(sql)
    return cursor.fetchone()


def insert(sql: str):
    conn, cursor = connect()
    cursor.execute(sql)
    conn.commit()
    return cursor.fetchone()
