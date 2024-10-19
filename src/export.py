from dotenv import load_dotenv, dotenv_values
from datetime import datetime
import os, json

from database import DatabaseHandler

def get_table_rows(database, table_name):
    columns = db_handler.execute_raw_sql("SHOW COLUMNS FROM {}.{} WHERE Extra = 'auto_increment';".format(database, table_name))
    if columns is None or len(columns) == 0:
        result = db_handler.execute_raw_sql("SELECT COUNT(*) AS 'rows' FROM {}.{}".format(database, table_name))
        return int(result[0]['rows'])

    field = columns[0]['Field']
    result = db_handler.execute_raw_sql("SELECT {} FROM {}.{} ORDER BY {} DESC LIMIT 1".format(field, database, table_name, field))
    return int(result[0][field])

if __name__ == "__main__":
    if not os.path.exists(".env"):
        raise Exception("Missing env file")

    dotenv_values(".env")
    load_dotenv()

    date = datetime.now().strftime('%Y%m%d')

    sql_files_directory = os.getenv("EXPORT_SQL_FILES_DIRECTORY")
    database = os.getenv("MYSQL_DATABASE")

    split_tables = os.getenv("TABLES_TO_SPLIT")
    split_rows = int(os.getenv("NUMBER_OF_ROWS_TO_SPLIT"))

    db_handler = DatabaseHandler()

    tables = db_handler.show_tables(database)
    for table in tables:
        table_name = table['name']

        table_rows = get_table_rows(database, table_name)

        if table_rows > split_rows and table_name in split_tables:
            size = round(table_rows / split_rows) + 1

            for i in range(size):
                backup_path = '{}/{}_{}_{}.sql'.format(
                    sql_files_directory,
                    table_name,
                    i,
                    date
                )

                if os.path.exists(backup_path):
                    print('Backup {} already exists'.format(backup_path))
                    continue

                rows_ini = split_rows * i
                rows_fin = (split_rows * (i + 1)) - 1

                print('Backup {} from {} to {}'.format(backup_path, rows_ini, rows_fin))
                db_handler.execute_backup(database, table_name, backup_path, rows_ini, rows_fin, i, True)
        else:
            backup_path = '{}/{}_{}.sql'.format(
                sql_files_directory,
                table_name,
                date
            )

            if os.path.exists(backup_path):
                print('Backup {} already exists'.format(backup_path))
                continue

            db_handler.execute_backup(database, table_name, backup_path, 0, table_rows)

        print('Table {} backup done!\n'.format(table_name))
