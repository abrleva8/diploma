import sqlite3


class DataBaseWorker:
    def __init__(self):
        self.conn = sqlite3.connect('../data/data_base.db')
        self.cur = self.conn.cursor()

    def __del__(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def check_user(self, login, password):
        self.cur.execute(f"SELECT id_user_type FROM user WHERE login = '{login}' AND password = '{password}'")
        return self.cur.fetchall()
