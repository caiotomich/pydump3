from dotenv import load_dotenv, dotenv_values
import os, subprocess

if __name__ == "__main__":
    if not os.path.exists(".env"):
        raise Exception("Missing env file")

    dotenv_values(".env")
    load_dotenv()

    sql_files_directory = os.getenv("IMPORT_SQL_FILES_DIRECTORY")

    mysql_host = os.getenv("MYSQL_HOST")
    mysql_port = os.getenv("MYSQL_PORT")
    mysql_user = os.getenv("MYSQL_USER")
    mysql_password = os.getenv("MYSQL_PASSWORD")
    mysql_database = os.getenv("MYSQL_DATABASE")

    for filename in os.listdir(sql_files_directory).sorted():
        if filename.endswith('.sql'):
            print(f"Importing {filename}...")
            file_path = os.path.join(sql_files_directory, filename)

            subprocess.run(
                f"mysql -u {mysql_user} -p{mysql_password} -h {mysql_host} -P {mysql_port} {mysql_database} < {file_path}",
                shell=True
            )

    print("All SQL files imported successfully.")
