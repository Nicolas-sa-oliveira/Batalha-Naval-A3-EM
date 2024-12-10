from modelos.fila import Fila

# DB da fila aplicando singleton.
class FilaDB():

    _instance : "FilaDB" = None
    _fila: Fila
    
    def __init__(self: "FilaDB"):
        self._fila = Fila()
    
    @classmethod
    def instance(cls):
        if(cls._instance is None):
            cls._instance = FilaDB()
        return cls._instance
    
    @classmethod
    def inscrever_jogador_na_fila(cls, jogador):
        cls.instance()._fila.inscrever_jogador(jogador)

    @classmethod
    def desinscrever_jogador_na_fila(cls, jogador):
        cls.instance()._fila.desinscrever_jogador(jogador)

    @classmethod
    def mostrar_jogadores_na_fila(cls):
        return cls.instance()._fila.mostrar_jogadores_inscritos()