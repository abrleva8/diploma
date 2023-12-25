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

    def insert_material(self, name):
        self.cur.execute("INSERT INTO raw_material(name) VALUES (?)", (name,))
        self.conn.commit()

    def get_properties(self):
        self.cur.execute("SELECT name FROM property")
        return self.cur.fetchall()

    def insert_property(self, name, unit):
        id_unit = self.get_id_unit(unit)[0][0]
        self.cur.execute("INSERT INTO property(name, id_unit) VALUES (?,?)", (name, id_unit))
        self.conn.commit()

    def get_conditions(self):
        self.cur.execute("SELECT name FROM condition")
        return self.cur.fetchall()

    def insert_condition(self, name, unit):
        id_unit = self.get_id_unit(unit)[0][0]
        self.cur.execute("INSERT INTO condition(name, id_unit) VALUES (?, ?)", (name, id_unit))
        self.conn.commit()

    def get_units(self):
        self.cur.execute("SELECT denote FROM unit")
        return self.cur.fetchall()

    def delete_material(self, name):
        self.cur.execute("DELETE FROM raw_material WHERE name = (?)", (name,))
        self.conn.commit()

    def delete_property(self, name):
        self.cur.execute("DELETE FROM property WHERE name = (?)", (name,))
        self.conn.commit()

    def delete_condition(self, name):
        self.cur.execute("DELETE FROM condition WHERE name = (?)", (name,))
        self.conn.commit()

    def get_id_unit(self, unit):
        self.cur.execute(f"SELECT id_unit FROM unit WHERE denote = '{unit}'")
        return self.cur.fetchall()
