from dotenv import load_dotenv, dotenv_values
from datetime import datetime
import shutil
import os

from database import DatabaseHandler

if __name__ == "__main__":
    if not os.path.exists(".env"):
        raise Exception("Missing env file")

    dotenv_values(".env")
    load_dotenv()

    date = datetime.now().strftime('%Y%m%d')
    database = os.getenv("BACKUP_DATABASE")
    path = os.getenv("BACKUP_PATH")
    split_rows = int(os.getenv("SPLIT_ROWS"))

    db_handler = DatabaseHandler()

    tables = db_handler.show_tables(database)
    for table in tables:
        table_name = table['name']

        print('Table {}'.format(table_name))
        result = db_handler.execute_raw_sql("SELECT COUNT(*) AS 'rows' FROM {}.{}".format(database, table_name))
        table_rows = int(result[0]['rows'])

        if table_rows > split_rows:
            size = round(table_rows / split_rows) + 1

            for i in range(size):
                backup_path = '{}/{}_{}_{}.sql'.format(path, table_name, i, date)

                if os.path.exists(backup_path):
                    print('Backup {} already exists'.format(backup_path))
                    continue

                print('Backup {} from {} to {}'.format(backup_path, split_rows * i, split_rows * (i + 1)))
                db_handler.execute_backup(database, table_name, backup_path, split_rows * i, split_rows * (i + 1))
        else:
            backup_path = '{}/{}_{}.sql'.format(path, table_name, date)

            if os.path.exists(backup_path):
                print('Backup {} already exists'.format(backup_path))
                continue

            db_handler.execute_backup(database, table_name, backup_path, 0, table_rows)

        print('Table {} backup done!\n'.format(table_name))
