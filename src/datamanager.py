# ==============================================================================
# Copyright 2023-* Marco Sciorilli. All Rights Reserved.
# Copyright 2023-* QRC @ Technology Innovation Institute of Abu Dhabi. All Rights Reserved.
# ==============================================================================


import sqlite3


def connect_database(name_database):
    conn = sqlite3.connect(f'{name_database}.db')
    return conn


def create_table(name_database, name_table, rows, unique):
    connection = connect_database(name_database)
    string_creation = create_table_string(name_table, rows, unique)
    cursor = connection.cursor()
    cursor.execute(string_creation)
    cursor.close()


def create_table_string(name_table, rows, unique):
    string = f'CREATE TABLE {name_table}('
    for i in rows:
        string = string + f'{i} {rows[i]}, '

    string = string + 'UNIQUE( '
    for j in unique:
        string = string + f'{j}, '
    size = len(string)
    string = string[:size - 2]
    string = string + '))'
    return string


def insert_value_table(name_database, name_table, row):
    connection = connect_database(name_database)
    cursor = connection.cursor()
    string_creation = create_insertion_string(name_table, row)
    cursor.execute(string_creation)
    connection.commit()
    cursor.close()


def create_insertion_string(name_table, row):
    string = f'INSERT OR REPLACE INTO {name_table} ( '
    for i in row:
        string = string + f'{i}, '
    size = len(string)
    string = string[:size - 2]
    string = string + ') VALUES ('
    for i in row:
        if type(row[i]) is str:
            string = string + f' \'{row[i]}\', '
        else:

            string = string + f'{row[i]}, '
    size = len(string)
    string = string[:size - 2]
    string = string + ')'
    return string


def read_data(name_database, name_table, data_to_read, parameters_to_fix):
    connection = connect_database(name_database)
    cursor = connection.cursor()
    string = create_reading_string(name_table, data_to_read, parameters_to_fix)
    rows = cursor.execute(string).fetchall()
    return rows


def create_reading_string(name_table, data_to_read, parameters_to_fix):
    string = 'SELECT '
    for i in data_to_read:
        string = string + f'{i}, '
    size = len(string)
    string = string[:size - 2]
    string = string + f" FROM {name_table} WHERE "
    for j in parameters_to_fix:
        if type(parameters_to_fix[j]) is str:
            string = string + f'{j}  = \'{parameters_to_fix[j]}\' AND '
        else:
            string = string + f'{j}  = {parameters_to_fix[j]} AND '
    size = len(string)
    string = string[:size - 4]
    return string
