import sqlite3


class Mysql(object):
    def __init__(self, db_name):
        try:
            self.conn = sqlite3.connect(db_name)
        except Exception as e:
            print(e)
        else:
            self.cur = self.conn.cursor()

    def create_table(self, sql):
        res = self.cur.execute(sql)

    def close(self):
        self.cur.close()
        self.conn.close()

    def add(self, sql, data):  # 增
        res = self.cur.executemany(sql, data)
        if res:
            self.conn.commit()
        else:
            self.conn.rollback()

    def rem(self, sql):  # 删
        res = self.cur.execute(sql)
        if res:
            self.conn.commit()
        else:
            self.conn.rollback()

    def mod(self, sql):  # 改
        res = self.cur.execute(sql)
        if res:
            self.conn.commit()
        else:
            self.conn.rollback()

    def show(self, sql):  # 查
        self.cur.execute(sql)
        res = self.cur.fetchall()
        return res
