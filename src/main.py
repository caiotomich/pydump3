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
    split_size = os.getenv("SPLIT_SIZE_MB")

    db_handler = DatabaseHandler()

    tables = db_handler.show_tables(database)
    for table in tables:
        table_name = table['name']

        print('Table {}'.format(table_name))
        if int(table['size']) > int(split_size):
            size = round(table['size'] / int(split_size))
            rows = round(table['rows'] / size) + 100
            for i in range(size):
                backup_path = '{}/{}_{}_{}.sql'.format(path, table_name, i, date)

                if os.path.exists(backup_path):
                    print('Backup {} already exists'.format(backup_path))
                    continue

                print('Backup {} from {} to {}'.format(backup_path, rows * i, rows * (i + 1)))
                db_handler.execute_backup(database, table_name, backup_path, rows * i, rows * (i + 1))
        else:
            backup_path = '{}/{}_{}.sql'.format(path, table_name, date)

            if os.path.exists(backup_path):
                print('Backup {} already exists'.format(backup_path))
                continue
            db_handler.execute_backup(database, table_name, backup_path, 0, table['rows'])

        print('Table {} backup done!\n'.format(table_name))
