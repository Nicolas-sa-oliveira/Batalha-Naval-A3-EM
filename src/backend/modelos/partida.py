from modelos.tabuleiro import Tabuleiro
from modelos.jogador import Jogador
import itertools

# Classe modelo da partida. Possui dois jogadores participantes e o tabuleiro.
class Partida():

    _id : int
    _jogador_a : Jogador
    _jogador_b : Jogador
    _tabuleiro : Tabuleiro
    _turno : int
    _repeticoes_jogadas: int
    _status: str

    # Utilizado para fazer um ID que se auto-incrementa a cada objeto criado.
    id_obj = itertools.count(1)

    def __init__(self, jogador_a: Jogador, jogador_b: Jogador):
        self._id = next(Partida.id_obj)
        self._jogador_a = jogador_a
        self._jogador_b = jogador_b
        self._tabuleiro = Tabuleiro()
        self._turno = 1
        self._repeticoes_jogadas = 0
        self._status = "preparacao"