import sqlite3


class MaterialDataBaseWorker:
    def __init__(self):
        # self.conn = sqlite3.connect(r"C:\Users\Ilia\PycharmProjects\diploma\data\materials.db")
        self.conn = sqlite3.connect(r"../data/materials.db")
        self.cur = self.conn.cursor()

    def __del__(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def get_materials(self):
        self.cur.execute("SELECT name FROM raw_material")
        return self.cur.fetchall()

    def insert_material(self, name: str):
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

    def insert_result(self, parameter_name, unit):
        id_unit = self.get_id_unit(unit)[0][0]
        self.cur.execute("INSERT INTO result(parameter_name, id_unit) VALUES (?, ?)",
                         (parameter_name, id_unit))
        self.conn.commit()

    def insert_unit(self, unit_denote):
        self.cur.execute("INSERT INTO unit(denote) VALUES (?)", (unit_denote,))
        self.conn.commit()

    def get_unit_by_property_name(self, property_name):
        self.cur.execute("SELECT denote\n"
                         "FROM unit\n"
                         "INNER JOIN property ON unit.id_unit = property.id_unit\n"
                         "WHERE property.name = (?);", (property_name,))
        return self.cur.fetchall()

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

    def delete_result(self, parameter_name):
        self.cur.execute("DELETE FROM result WHERE parameter_name = (?)", (parameter_name,))
        self.conn.commit()

    def delete_unit(self, unit_denote: str):
        self.cur.execute("DELETE FROM unit WHERE denote = (?)", (unit_denote,))
        self.conn.commit()

    def get_id_unit(self, unit):
        self.cur.execute(f"SELECT id_unit FROM unit WHERE denote = '{unit}'")
        return self.cur.fetchall()

    def get_results(self):
        self.cur.execute("SELECT parameter_name FROM result")
        return self.cur.fetchall()

    def edit_unit(self, curr_unit_denote: str, new_unit_denote: str):
        self.cur.execute(f"UPDATE unit SET denote = (?) WHERE denote = (?)", (new_unit_denote, curr_unit_denote))
        self.conn.commit()

    def get_full_dataset(self):
        self.cur.executescript("DROP TABLE IF EXISTS TEMP_TABLE_DENSITY;\n"
                               "CREATE TEMPORARY TABLE TEMP_TABLE_DENSITY AS\n"
                               "SELECT raw_material.name, value AS density\n"
                               "FROM raw_material_property\n"
                               "INNER JOIN raw_material "
                               "    ON raw_material_property.id_raw_material = raw_material.id_raw_material\n"
                               "INNER JOIN property"
                               "    ON raw_material_property.id_property = property.id_property\n"
                               "WHERE property.name = 'плотность';\n"
                               "\n"
                               "DROP TABLE IF EXISTS TEMP_TABLE_CONTAINS_350;\n"
                               "CREATE TEMPORARY TABLE TEMP_TABLE_CONTAINS_350 AS\n"
                               "SELECT raw_material.name, value AS contain\n"
                               "FROM raw_material_property\n"
                               "INNER JOIN raw_material"
                               "    ON raw_material_property.id_raw_material = raw_material.id_raw_material\n"
                               "INNER JOIN property ON raw_material_property.id_property = property.id_property\n"
                               "                            WHERE property.name = 'содержание 350+';\n"
                               "                            \n"
                               "                            DROP TABLE IF EXISTS TEMP_TABLE_CONTAINS_ASPHALTENE;\n"
                               "                            CREATE TEMPORARY TABLE TEMP_TABLE_CONTAINS_ASPHALTENE AS\n"
                               "                            SELECT raw_material.name, value AS asphaltene_contain\n"
                               "                            FROM raw_material_property\n"
                               "INNER JOIN raw_material ON raw_material_property.id_raw_material = "
                               "raw_material.id_raw_material\n"
                               "INNER JOIN property ON raw_material_property.id_property = property.id_property\n"
                               "                            WHERE property.name = 'содержание асфальтенов';\n"
                               "                            \n"
                               "                            DROP TABLE IF EXISTS TEMP_TABLE_RESEARCH;\n"
                               "                            CREATE TEMPORARY TABLE TEMP_TABLE_RESEARCH AS\n"
                               "SELECT raw_material.name, condition_in_set.value AS pressure, research.value AS "
                               "result\n"
                               "                            FROM condition_in_set\n"
                               "INNER JOIN research ON condition_in_set.id_condition_set = research.id_condition_set\n"
                               "INNER JOIN raw_material ON raw_material.id_raw_material = research.id_raw_material\n"
                               "                            WHERE id_result = 1;\n"
                               "                            \n"
                               "                            \n"
                               "SELECT TEMP_TABLE_DENSITY.name, TEMP_TABLE_DENSITY.density, "
                               "TEMP_TABLE_CONTAINS_350.contain, TEMP_TABLE_CONTAINS_ASPHALTENE.asphaltene_contain\n"
                               "                            FROM TEMP_TABLE_DENSITY\n"
                               "INNER JOIN TEMP_TABLE_CONTAINS_350 ON TEMP_TABLE_DENSITY.name = "
                               "TEMP_TABLE_CONTAINS_350.name\n"
                               "INNER JOIN TEMP_TABLE_CONTAINS_ASPHALTENE ON TEMP_TABLE_DENSITY.name = "
                               "TEMP_TABLE_CONTAINS_ASPHALTENE.name;\n"
                               )

        cursor = self.cur.execute(
            "SELECT TEMP_TABLE_DENSITY.name as `Название`, density as `Плотность`,"
            "pressure as `Давление`, contain as `Содержание 350+`,"
            "asphaltene_contain as `Содержание асфальтенов`, result as `Результат`\n"
            "FROM TEMP_TABLE_DENSITY\n"
            "INNER JOIN TEMP_TABLE_RESEARCH ON TEMP_TABLE_DENSITY.name = TEMP_TABLE_RESEARCH.name\n"
            "INNER JOIN TEMP_TABLE_CONTAINS_350 ON TEMP_TABLE_DENSITY.name = "
            "TEMP_TABLE_CONTAINS_350.name\n"
            "INNER JOIN TEMP_TABLE_CONTAINS_ASPHALTENE on TEMP_TABLE_CONTAINS_350.name = "
            "TEMP_TABLE_CONTAINS_ASPHALTENE.name;"
        )

        names = [fields[0] for fields in cursor.description]

        return names, self.cur.fetchall()
