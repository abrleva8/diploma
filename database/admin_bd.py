import sqlite3


class UserDataBaseWorker:
    def __init__(self):
        # self.conn = sqlite3.connect(r"C:\Users\Ilia\PycharmProjects\diploma\data\users.db")
        self.conn = sqlite3.connect(r"../data/users.db")
        self.cur = self.conn.cursor()

    def __del__(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def check_user(self, login, password):
        self.cur.execute(f"SELECT id_user_type FROM user WHERE login = '{login}' AND password = '{password}'")
        return self.cur.fetchall()

    def get_logins(self):
        self.cur.execute("SELECT login FROM user")
        return self.cur.fetchall()

    def get_user_types(self):
        self.cur.execute("SELECT name FROM user_type")
        return self.cur.fetchall()

    def insert_login(self, login, password, user_type):
        user_type_id = self.get_user_type_id(user_type)[0][0]
        self.cur.execute(f"INSERT INTO user (login, password, id_user_type) VALUES"
                         f"('{login}', '{password}', '{user_type_id}')")
        self.conn.commit()

    def get_user_type_id(self, user_type):
        self.cur.execute(f"SELECT id_user_type FROM user_type WHERE name = '{user_type}'")
        return self.cur.fetchall()

    def delete_user(self, login):
        self.cur.execute(f"DELETE FROM user WHERE login = '{login}'")
        self.conn.commit()
