import os
import pymysql

UNIX_SOCKET = os.environ["INSTANCE_UNIX_SOCKET"]
DB_USER = os.environ["DB_USER"]
DB_PASS = os.environ["DB_PASS"]
DB_NAME = os.environ["DB_NAME"]


def connect():
    db = pymysql.connect(
        user=DB_USER,
        password=DB_PASS,
        unix_socket=UNIX_SOCKET,
        db=DB_NAME
    )
    return db


def execute(sql, data=None):
    db = connect()
    with db.cursor() as cur:
        cur.execute(sql, data)
    db.commit()
    db.close()


def select(sql, data=None):
    db = connect()
    with db.cursor(pymysql.cursors.DictCursor) as cur:
        cur.execute(sql, data)
        rows = cur.fetchall()
    db.close()
    return rows


def selectOne(sql, data=None):
    db = connect()
    with db.cursor(pymysql.cursors.DictCursor) as cur:
        cur.execute(sql, data)
        row = cur.fetchone()
    db.close()
    return row
