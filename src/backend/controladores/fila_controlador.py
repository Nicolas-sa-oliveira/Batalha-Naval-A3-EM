from src.backend.persistencia.fila_db import FilaDB
from src.backend.controladores.jogador_controlador import JogadorControlador
from src.backend.controladores.partida_controlador import PartidaControlador
from enum import Enum 

# Classe para definir erros do controlador da fila.
class FilaControladorErro(Enum):
    JOGADOR_NAO_EXISTENTE = 0 
    #======================================== Retorna erro caso o jogador não esteja registrado e tente se inscrever

# Controlador da fila
class FilaControlador:

    @classmethod
    def inscrever_na_fila(cls, nome_jogador: str):
        lista_de_jogadores = JogadorControlador.listar_todos_os_jogadores()
        jogador = None

        fila = FilaDB.instance().mostrar_jogadores_na_fila()
        for jogador in fila:
            if jogador['nome'] == nome_jogador:
                return {"message": "Você já está na fila"}

        checagem_de_partida = PartidaControlador.checar_jogador_em_partida(nome_jogador)
        if (checagem_de_partida["message"] != "Você não está em fila e nem em uma partida"):
            return {"message": "Você já está em uma partida"}
        
        for j in lista_de_jogadores:
            if j['nome'] == nome_jogador:
                jogador = j

        if(jogador != None):
            FilaDB.instance().inscrever_jogador_na_fila(jogador)
            jogadores_das_partidas = cls.checar_estado_da_fila()
            if (jogadores_das_partidas):
                while (len(jogadores_das_partidas) / 2) > 0:
                    PartidaControlador.começar_nova_partida(jogadores_das_partidas[0], jogadores_das_partidas[1])
                    for _ in range(2): jogadores_das_partidas.pop(0)
            return True
        else:
            return FilaControladorErro.JOGADOR_NAO_EXISTENTE
    
    @classmethod
    def desinscrever_da_fila(cls, nome_jogador: str):    
        lista_de_jogadores = JogadorControlador.listar_todos_os_jogadores()
        jogador = None
        
        for j in lista_de_jogadores:
            if j['nome'] == nome_jogador:
                jogador = j
        
        if(jogador != None):
            return FilaDB.instance().desinscrever_jogador_na_fila(jogador)
        else:
            return FilaControladorErro.JOGADOR_NAO_EXISTENTE
        
    @classmethod
    def mostrar_jogadores_na_fila(cls):
        return FilaDB.instance().mostrar_jogadores_na_fila()
    
    @classmethod
    def checar_estado_da_fila(cls):
        fila = FilaDB.instance().mostrar_jogadores_na_fila()
        jogadores : list = []
        
        while len(fila) >= 2:
            jogadores.append(fila[0])
            jogadores.append(fila[1])
            cls.desinscrever_da_fila(fila[0]['nome'])
            cls.desinscrever_da_fila(fila[1]['nome'])
            fila = FilaDB.instance().mostrar_jogadores_na_fila()
            
        if jogadores != []:
            return jogadores
        return False
    
    # Precisa da partida - Método para checar se seu nome está na fila e se sua partida começou
    @classmethod
    def checar_confirmacao_da_partida(cls, nome_jogador: str):
        fila = FilaDB.instance().mostrar_jogadores_na_fila()

        for jogador in fila:
            if jogador['nome'] == nome_jogador:
                return {"message": "Aguardando jogadores para partida"}
        return PartidaControlador.checar_jogador_em_partida(nome_jogador)
