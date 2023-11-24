import pymysql
import os

class DatabaseHandler:
    def __init__(self):
        self.host = os.getenv("MYSQL_HOST")
        self.user = os.getenv("MYSQL_USER")
        self.password = os.getenv("MYSQL_PASSWORD")

        self.stmt = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    def execute_raw_sql(self, query):
        with self.stmt.cursor() as cursor:
            cursor.execute(query)
            databases = cursor.fetchall()
        self.stmt.close()

        return databases

    def show_databases(self):
        return self.execute_raw_sql("SHOW DATABASES")

    def execute_backup(self, database, path):
        os.popen("mysqldump -u{} -p{} -h {} -e --opt -c {} > {}".format(
                self.user, self.password, self.host, database, path
            )
        )
