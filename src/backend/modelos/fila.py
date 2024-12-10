from src.backend.modelos.jogador import Jogador

# Classe modelo para fila para entrar em partidas. Usa métodos de inscrição e desinscrição.
class Fila():
    _jogadores : list[Jogador]

    def __init__(self):
        self._jogadores = []
    
    def __str__(self):
        contagem = len(self._jogadores)
        return f"Quantidade de jogadores na fila: {contagem}"
    
    def inscrever_jogador(self, jogador):
        self._jogadores.append(jogador)
    
    def desinscrever_jogador(self, jogador):
        self._jogadores = [j for j in self._jogadores if j['nome'] != jogador['nome']]

    def mostrar_jogadores_inscritos(self):
        return self._jogadores