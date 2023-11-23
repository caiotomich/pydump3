import os
import re
import shutil
import pymysql.cursors
from datetime import datetime, timedelta

# informações de conexão
host = '127.0.0.1'
usuario = 'admin'
senha = 'admin'

# diretórios de backup
path_backup = 'd:\\'
path_backup_01 = 'd:\\_backup\\mysql\\'

# efetua conexão com a base de dados
stmt = pymysql.connect(
    host=host,
    user=usuario,
    password=senha,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

# carrega bases de dados do mysql
with stmt.cursor() as cursor:
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()

# lista todas as bases de dados
for i in databases:
    # bases de dados padrão que devem ser ignoradas
    default_databases = ['sys', 'mysql', 'test', 'performance_schema', 'information_schema']

    # ignora bases de dados padrão
    if i['Database'] in default_databases:
        continue

    # nome do arquivo de backup (compactado)
    arquivo_backup = i['Database'] + '_' + datetime.now().strftime('%Y%m%d') + '.sql'
    path_arquivo_backup = path_backup + arquivo_backup

    # executa backup das bases de dados
    os.popen("mysqldump -u{} -p{} -h {} -e --opt -c {} > {}".format(
            usuario, senha, host, i['Database'], path_arquivo_backup
        )
    )

    # executa cópias
    # shutil.copy(path_arquivo_backup, path_backup_01 + arquivo_backup)
    print(i['Database'], arquivo_backup)
