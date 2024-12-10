import sqlite3

# Classe para configuração do banco de dados sqlite.
class ConfigDB():

    @classmethod
    def executa_sql(cls, codigo_sql, valores):
        with sqlite3.connect("../../batalha_naval.sqlite") as conn:
            if (valores != False):
                try:
                    cursor = conn.cursor()
                    return cursor.execute(codigo_sql, valores)
                except sqlite3.Error as e:
                    print(e)
            else:
                try:
                    cursor = conn.cursor()
                    return cursor.execute(codigo_sql)
                except sqlite3.Error as e:
                    print(e)