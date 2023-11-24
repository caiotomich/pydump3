from dotenv import load_dotenv, dotenv_values
from datetime import datetime
import os

from database import DatabaseHandler

if __name__ == "__main__":
    dotenv_values(".env")
    load_dotenv()

    path = os.getenv("BACKUP_PATH")
    ignore_databases = os.getenv("IGNORE_DATABASES") if os.getenv("IGNORE_DATABASES") else []
    default_databases = ['sys', 'mysql', 'test', 'performance_schema', 'information_schema']

    db_handler = DatabaseHandler()

    databases = db_handler.show_databases()
    for item in databases:
        database_name = item['Database']

        if database_name in default_databases or database_name in ignore_databases:
            continue

        date = datetime.now().strftime('%Y%m%d')
        backup_path = '{}/{}_{}.sql'.format(path, database_name, date)

        db_handler.execute_backup(database_name, path)

        # executa cópias
        # shutil.copy(path_arquivo_backup, path_backup_01 + arquivo_backup)

        print(database_name, backup_path)
