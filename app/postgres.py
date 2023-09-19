import psycopg2
from psycopg2 import extras
from app.config import DBNAME, DBUSER, PASSWORD


insert_query = '''
INSERT INTO user_logins(
    user_id,
    device_type,
    masked_ip,
    masked_device_id,
    locale,
    app_version,
    create_date)
VALUES %s'''

def entry_to_tuple(entry):
    return tuple(entry.get(field, 'NULL') for field in (
        'user_id',
        'device_type',
        'ip',
        'device_id',
        'locale',
        'app_version'
        )
    ) + ('NOW()',)

def db_connect(dbname=DBNAME, user=DBUSER, password=PASSWORD):
    conn = psycopg2.connect(dbname=dbname, user=user, password=password)
    cursor = conn.cursor()
    return conn, cursor
def change_column_type(column='app_version', new_type='varchar(20)'):
    conn, cursor = db_connect()
    cursor = conn.cursor()
    cursor.execute(f'ALTER TABLE user_logins ALTER COLUMN {column} TYPE {new_type}')
    conn.commit()
    conn.close()
def insert_postgres(entries):
    conn, cursor = db_connect()
    data_to_insert = tuple(entry_to_tuple(entry) for entry in entries)
    for entry in data_to_insert:
        print(entry)
    extras.execute_values(cursor, insert_query, data_to_insert)
    conn.commit()

