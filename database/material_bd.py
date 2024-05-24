import os.path
import sqlite3


class MaterialDataBaseWorker:
    def __init__(self):
        # path = os.path.join(os.getcwd(), 'data', 'materials.db')
        path = r'C:\Users\Ilia\PycharmProjects\diploma\data\materials.db'
        self.conn = sqlite3.connect(path)
        self.cur = self.conn.cursor()

    def __del__(self):
        try:
            self.conn.commit()
            self.cur.close()
            self.conn.close()
        except AttributeError:
            pass

    def get_materials(self):
        self.cur.execute("SELECT name FROM raw_material")
        return self.cur.fetchall()

    def get_material_types(self):
        self.cur.execute("SELECT type_name FROM type")
        return self.cur.fetchall()

    def insert_material(self, material_name: str, type_id: int):
        self.cur.execute("INSERT INTO raw_material(name, id_type) VALUES (?, ?)", (material_name, type_id))
        self.conn.commit()

    def get_properties(self, unit: bool = False) -> list[tuple[str, str]]:
        if unit:
            self.cur.execute("SELECT name, denote FROM property INNER JOIN unit ON property.id_unit = unit.id_unit")
        else:
            self.cur.execute("SELECT name FROM property")
        return self.cur.fetchall()

    def get_types(self):
        self.cur.execute("SELECT type_name FROM type")
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

    def insert_type(self, type_name: str) -> None:
        self.cur.execute("INSERT INTO type(type_name) VALUES (?)", (type_name,))
        self.conn.commit()

    def insert_raw_material_property(self, id_raw_material: int, id_property: int, value: float) -> None:
        self.cur.execute("INSERT INTO raw_material_property(id_raw_material, id_property, value) VALUES (?, ?, ?)",
                         (id_raw_material, id_property, value))
        self.conn.commit()

    def get_unit_by_property_name(self, property_name):
        self.cur.execute("SELECT denote\n"
                         "FROM unit\n"
                         "INNER JOIN property ON unit.id_unit = property.id_unit\n"
                         "WHERE property.name = (?);", (property_name,))
        return self.cur.fetchall()

    def get_unit_by_condition_name(self, condition_name: str):
        self.cur.execute("SELECT denote\n"
                         "FROM unit\n"
                         "INNER JOIN condition ON unit.id_unit = condition.id_unit\n"
                         "WHERE condition.name = (?);", (condition_name,))
        return self.cur.fetchall()

    def get_unit_by_result_name(self, result_name):
        self.cur.execute("SELECT denote\n"
                         "FROM unit\n"
                         "INNER JOIN result ON unit.id_unit = result.id_unit\n"
                         "WHERE result.parameter_name = (?);", (result_name,))
        return self.cur.fetchall()

    def get_type_id_by_type_name(self, type_name: str) -> list[tuple[int,]]:
        self.cur.execute("SELECT id_type\n"
                         "FROM type\n"
                         "WHERE type.type_name = (?);", (type_name,))
        return self.cur.fetchall()

    def get_type_id_by_material_name(self, material_name: str) -> list[tuple[int,]]:
        self.cur.execute("SELECT type_name\n"
                         "FROM raw_material\n"
                         "INNER JOIN type ON raw_material.id_type = type.id_type\n"
                         "WHERE name = (?);", (material_name,))
        return self.cur.fetchall()

    def get_id_material_by_material_name(self, material_name):
        self.cur.execute("SELECT id_raw_material\n"
                         "FROM raw_material\n"
                         "WHERE raw_material.name = (?);", (material_name,))
        return self.cur.fetchall()

    def get_id_property_by_property_name(self, property_name):
        self.cur.execute("SELECT id_property\n"
                         "FROM property\n"
                         "WHERE property.name = (?);", (property_name,))
        return self.cur.fetchall()

    def get_result_id_by_result_name(self, result_name):
        self.cur.execute("SELECT id_result\n"
                         "FROM result\n"
                         "WHERE result.parameter_name = (?);", (result_name,))
        return self.cur.fetchall()

    def get_units(self):
        self.cur.execute("SELECT denote FROM unit")
        return self.cur.fetchall()

    def get_name_and_value_by_material_name(self, material_name: str) -> list[tuple[str, float]]:
        self.cur.execute("SELECT property.name, value\n"
                         "FROM raw_material_property\n"
                         "INNER JOIN property ON raw_material_property.id_property = property.id_property\n"
                         "INNER JOIN raw_material ON raw_material_property.id_raw_material = "
                         "raw_material.id_raw_material\n"
                         "WHERE raw_material.name = (?);", (material_name,))
        return self.cur.fetchall()

    def delete_type(self, type_name: str) -> None:
        self.cur.execute("DELETE FROM type WHERE type_name = (?)", (type_name,))
        self.conn.commit()

    def delete_material(self, material_name: str) -> None:
        self.cur.execute("DELETE\n"
                         "FROM raw_material_property\n"
                         "WHERE id_raw_material = (\n"
                         "SELECT id_raw_material\n"
                         "FROM raw_material\n"
                         "WHERE name = (?)\n"
                         ");", (material_name,))
        self.cur.execute("DELETE FROM raw_material WHERE name = (?)", (material_name,))
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

    def edit_material(self, curr_material_name: str, new_material_name: str, new_type_name: str) -> None:
        self.cur.execute("UPDATE raw_material\n"
                         "SET name = (?), id_type = (\n"
                         "SELECT id_type\n"
                         "FROM type\n"
                         "WHERE type_name = (?)\n"
                         ")\n"
                         "WHERE name = (?);", (new_material_name, new_type_name, curr_material_name))
        self.conn.commit()

    def edit_raw_material_property(self, material_name: str, property_name: str, new_value: float) -> None:
        self.cur.execute("UPDATE raw_material_property\n"
                         "SET value = (?)\n"
                         "WHERE id_raw_material = (\n"
                         "SELECT id_raw_material\n"
                         "FROM raw_material\n"
                         "WHERE name = (?)\n"
                         ")\n"
                         "AND\n"
                         "id_property = (\n"
                         "SELECT id_property\n"
                         "FROM property\n"
                         "WHERE name = (?))", (new_value, material_name, property_name))
        self.conn.commit()

    def edit_type(self, curr_type_name: str, new_type_name: str) -> None:
        self.cur.execute(f"UPDATE type SET type_name = (?) WHERE type_name = (?)", (new_type_name, curr_type_name))
        self.conn.commit()

    def edit_result(self, current_result_name: str, current_unit_name: str, new_result_name: str, new_unit_name: str):
        curr_id_unit = self.get_id_unit(current_unit_name)[0][0]
        new_id_unit = self.get_id_unit(new_unit_name)[0][0]
        self.cur.execute('UPDATE result\n'
                         f'SET parameter_name = (?), id_unit = (?)\n'
                         f'WHERE parameter_name = (?) AND id_unit = (?)',
                         (new_result_name, new_id_unit, current_result_name, curr_id_unit))

    def edit_condition(self, current_condition_name: str, current_unit_name: str,
                       new_condition_name: str, new_unit_name: str):
        self.cur.execute('UPDATE condition\n'
                         'SET name = (?) , id_unit = (\n'
                         'SELECT id_unit\n'
                         'FROM unit\n'
                         'WHERE denote = (?)\n'
                         ')\n'
                         'WHERE name = (?) AND id_unit = (\n'
                         'SELECT id_unit\n'
                         'FROM unit\n'
                         'WHERE denote = (?)\n'
                         ')',
                         (new_condition_name, new_unit_name, current_condition_name, current_unit_name))
        return self.cur.rowcount

    def edit_property(self, current_property_name: str, current_unit_name: str, new_property_name: str,
                      new_unit_name: str):
        curr_id_unit = self.get_id_unit(current_unit_name)[0][0]
        new_id_unit = self.get_id_unit(new_unit_name)[0][0]
        self.cur.execute('UPDATE property\n'
                         f'SET name = (?), id_unit = (?)\n'
                         f'WHERE name = (?) AND id_unit = (?)',
                         (new_property_name, new_id_unit, current_property_name, curr_id_unit))

    # TODO: подумать как это будет выглядеть в общем виде
    def get_full_dataset(self, filter_type: str, result: str):
        id_result = self.get_result_id_by_result_name(result)[0][0]

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
                               f"                            WHERE id_result = {id_result};\n"
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

        sql_query = f"""
            SELECT TEMP_TABLE_DENSITY.name as `Название`, type.type_name as `Тип`, density as `Плотность`,
            pressure as `Давление`, contain as `Содержание 350+`, asphaltene_contain as `Содержание асфальтенов`,
            result as {result}
            FROM TEMP_TABLE_DENSITY
            INNER JOIN TEMP_TABLE_RESEARCH
                ON TEMP_TABLE_DENSITY.name = TEMP_TABLE_RESEARCH.name
            INNER JOIN TEMP_TABLE_CONTAINS_350
                ON TEMP_TABLE_DENSITY.name = TEMP_TABLE_CONTAINS_350.name
            INNER JOIN TEMP_TABLE_CONTAINS_ASPHALTENE
                ON TEMP_TABLE_CONTAINS_350.name = TEMP_TABLE_CONTAINS_ASPHALTENE.name
            LEFT JOIN raw_material
                ON raw_material.name = TEMP_TABLE_DENSITY.name
            LEFT JOIN type
                ON raw_material.id_type = type.id_type
        """

        if filter_type != 'Все':
            sql_query += '\nWHERE type_name = (?);'
            __params = (filter_type,)
        else:
            __params = None

        if __params:
            cursor = self.cur.execute(sql_query, __params)
        else:
            cursor = self.cur.execute(sql_query)

        names = [fields[0] for fields in cursor.description]

        return names, self.cur.fetchall()
