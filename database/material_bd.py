import sqlite3


class MaterialDataBaseWorker:
    def __init__(self):
        self.conn = sqlite3.connect('../data/materials.db')
        self.cur = self.conn.cursor()

    def __del__(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def get_materials(self):
        self.cur.execute("SELECT name FROM raw_material")
        return self.cur.fetchall()

    def get_properties(self):
        self.cur.execute("SELECT name FROM property")
        return self.cur.fetchall()

    def get_conditions(self):
        self.cur.execute("SELECT name FROM condition")
        return self.cur.fetchall()
