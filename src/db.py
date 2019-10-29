# db서버와 연결하는 모듈

import psycopg2 as pg2
from src import Setting

conn = pg2.connect(Setting.db_setting.connection_setting)
conn.autocommit = True
cur = conn.cursor()

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

