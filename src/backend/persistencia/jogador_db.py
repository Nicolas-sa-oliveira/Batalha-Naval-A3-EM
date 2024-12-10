from modelos.jogador import Jogador
from persistencia.config_db import ConfigDB

# DB do jogador aplicando singleton. Salva mudanças no banco de dados.
class JogadorDB():

    _instance = None
    _lista_de_jogadores : list = []

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = JogadorDB()
            cls._instance.popular_do_banco()
        return cls._instance

    @classmethod
    def popular_do_banco(cls):

        res = ConfigDB.executa_sql("SELECT id, nome, email, senha, pontuacao FROM Jogadores", False)

        for r in res:
            j : Jogador = Jogador(
                nome=r[1],
                email=r[2],
                senha=r[3]
            )
            j._pontuacao_acumulada = r[4]
            cls.get_instance()._lista_de_jogadores.append(j)

    @classmethod
    def listar_todos_os_jogadores(cls):
        return  cls.get_instance()._lista_de_jogadores
    
    @classmethod
    def inserir_jogador_no_banco(cls, jogador: Jogador):
        sqlite_insert = """INSERT INTO Jogadores (nome, pontuacao, email, senha) VALUES (?, ?, ?, ?);"""
        valores = (jogador._nome, jogador._pontuacao_acumulada, jogador._email, jogador._senha)
        ConfigDB.executa_sql(sqlite_insert, valores)
        
        cls.get_instance()._lista_de_jogadores.append(jogador)
    
    @classmethod
    def editar_jogador_no_banco(cls, nome: str, email: str):
        lista_filtrada : list[Jogador] = [x for x in  cls.get_instance()._lista_de_jogadores if x._nome == nome]
        if(len(lista_filtrada) == 0):
            return False
        else:
            jogador_alvo : Jogador = lista_filtrada[0]
            jogador_alvo._email = email

            sqlite_update = """UPDATE Jogadores SET email = ? where nome = ?"""
            valores = (jogador_alvo._email, jogador_alvo._nome)
            ConfigDB.executa_sql(sqlite_update, valores)

            return True
        
    @classmethod
    def edita_senha_no_banco(cls, nome: str, nova_senha: str):
        lista_filtrada : list[Jogador] = [x for x in  cls.get_instance()._lista_de_jogadores if x._senha == nova_senha]
        if(len(lista_filtrada) == 0):
            return False
        else:
            jogador_alvo : Jogador = lista_filtrada[0]
            jogador_alvo._senha = nova_senha

            sqlite_update = """UPDATE Jogadores SET senha = ? where nome = ?"""
            valores = (jogador_alvo._senha, jogador_alvo._nome)
            ConfigDB.executa_sql(sqlite_update, valores)

            return True

    @classmethod
    def remover_jogador_do_banco(cls, nome: str):
        cls.get_instance()._lista_de_jogadores = [p for p in  cls.get_instance()._lista_de_jogadores if p._nome != nome]
        valor = (nome,)
        sqlite_delete = """DELETE FROM Jogadores where nome = ?"""
        ConfigDB.executa_sql(sqlite_delete, valor)

    @classmethod
    def aumentar_pontuacao_por_nome(cls, nome: str):
        lista_filtrada : list[Jogador] = [x for x in  cls.get_instance()._lista_de_jogadores if x._nome == nome]
        if(len(lista_filtrada) == 0):
            return False
        else:
            jogador_alvo : Jogador = lista_filtrada[0]
            jogador_alvo._pontuacao_acumulada += 1

            sqlite_update = """UPDATE Jogadores SET pontuacao = ? where nome = ?"""
            valores = (jogador_alvo._pontuacao_acumulada, jogador_alvo._nome)
            ConfigDB.executa_sql(sqlite_update, valores)

            return True