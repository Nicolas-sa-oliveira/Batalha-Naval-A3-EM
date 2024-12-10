import os
import sqlite3

class ConfigDB:
    # Lê a variável de ambiente DATABASE_PATH, ou usa um caminho padrão se não estiver configurado
    DATABASE_PATH = os.getenv("DATABASE_PATH", "batalha_naval.sqlite")

    @classmethod
    def executa_sql(cls, codigo_sql, valores):
        try:
            with sqlite3.connect(cls.DATABASE_PATH) as conn:
                cursor = conn.cursor()
                if valores:
                    return cursor.execute(codigo_sql, valores)
                else:
                    return cursor.execute(codigo_sql)
        except sqlite3.Error as e:
            print(f"Erro ao acessar o banco de dados: {e}")
            return None
