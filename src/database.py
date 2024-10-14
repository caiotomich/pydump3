import pymysql
import os

class DatabaseHandler:
    def __init__(self):
        self.host = os.getenv("MYSQL_HOST")
        self.user = os.getenv("MYSQL_USER")
        self.password = os.getenv("MYSQL_PASSWORD")

        self.stmt = self.connect()

    def connect(self):
        try:
            return pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except pymysql.MySQLError as e:
            print(f"Error connecting to database: {e}")
            return None

    def execute_raw_sql(self, query):
        if self.stmt is None:
            self.stmt = self.connect()

        try:
            with self.stmt.cursor() as cursor:
                self.stmt.ping(reconnect=True)
                cursor.execute(query)
                result = cursor.fetchall()
                return result
        except pymysql.MySQLError as e:
            print(f"Error executing query: {e}")
        finally:
            self.stmt.close()

    def show_tables(self, database):
        return self.execute_raw_sql("SELECT \
                table_name AS 'name', \
                ROUND((data_length + index_length) / 1024 / 1024, 2) AS 'size', \
                ROUND(data_length / 1024 / 1024, 2) AS 'data_size', \
                ROUND(index_length / 1024 / 1024, 2) AS 'index_size' \
            FROM  \
                information_schema.tables \
            WHERE  \
                table_schema = '{}' \
                AND table_type = 'BASE TABLE' \
            ORDER BY \
                (data_length + index_length) DESC; \
        ".format(database))

    def execute_backup(self, database, table, path, limit_start, limit_end, split=False):
        mysqldump = "mysqldump -u{} -p{} -h {} -e --opt -c {} {} > {}".format(
                self.user, self.password, self.host, database, table, path, limit_start, limit_end
            )

        mysqldump_split = "mysqldump -u{} -p{} -h {} -e --opt -c {} {} > {} --where=\"id BETWEEN {} AND {}\"".format(
                self.user, self.password, self.host, database, table, path, limit_start, limit_end
            )
        
        command = mysqldump if split is False else mysqldump_split

        process = os.popen(command)
        output = process.read()
        process.close()
