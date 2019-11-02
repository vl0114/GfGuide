# db서버와 연결하는 모듈

import psycopg2 as pg2
import psycopg2.extras as pg2e
from src import Setting

conn = pg2.connect(Setting.db_setting.connection_setting)
conn.autocommit = True
cur = conn.cursor()
cur_dict = conn.cursor(cursor_factory=pg2e.DictCursor)


class psql:
    def __init__(self):
        self.conn = conn
        self.cur = cur

    def send(self, q):  # 구문 전송
        self.cur.execute(q)

    def get(self, q):  # 구문 전송후 결과 수신
        self.cur.execute(q)
        return self.cur.fetchall()

    def commit(self):  # 커밋
        self.conn.commit()


class psql2:
    def __init__(self):
        self.conn = conn
        self.cur = cur_dict

    def send(self, q):  # 구문 전송
        self.cur.execute(q)

    def get(self, q):  # 구문 전송후 결과 수신
        self.cur.execute(q)
        return self.cur.fetchall()

    def commit(self):  # 커밋
        self.conn.commit()


class Query:
    def dict_to_select(self, data: dict, db_from: str, keys: list = None, where=None):
        if keys is None:
            key = data.keys()
        else:
            key = keys
        _key = ','.join(key)

        w = 'select {} from {}'.format(_key, db_from)

        if where is not None:
            w = w + f' where {where}'

        return w

    def dict_to_insert(self, data: dict, db_into: str):
        _r = str()

        for i in data.values():
            if isinstance(i, list):
                _x = "'{ "
                for j in i:
                    _x = _x + (str(j) + ",")
                _x = _x[:-1]
                _x = _x + "}'"
                _r = _r + _x + ","
            else:
                _r = (_r + "'" + str(i) + "'" + ",")
        _r = _r[:-1]

        return 'insert into {} ({}) values({})'.format(
            db_into,
            ','.join((data.keys())),
            _r
        )

    def dict_to_update(self, data: dict, db_update: str, where: str):

        _r = ''

        for _k in data.keys():
            _v = data[_k]
            if isinstance(_v, list):
                _x = "'{ "
                for i in _v:
                    _x = _x + i + ","
                _x = _x[:-1]
                _x = _x + "}'"

                _r = _r + _k + '=' + _x + ","

            else:
                _r = _r + _k + "='{}'".format(str(_v)) + ","

        _r = _r[:-1]

        return 'update {} set {} where {}'.format(
            db_update, _r, where
        )
