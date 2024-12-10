from src.backend.persistencia.autenticacao_db import AutenticacaoDB
from src.backend.controladores.jogador_controlador import JogadorControlador
from enum import Enum
import hashlib

# Classe para definir erros do controlador de auntenticações.
class AutenticacaoErros(Enum):
    USUARIO_OU_SENHA_INCORRETOS = 1
    AUTENTICACAO_OK = 2

# Controlador de auntenticações.
class AutenticacaoControlador:
    
    @classmethod
    def autenticar(cls, nome: str, senha: str):

        lista_de_jogadores = JogadorControlador.pegar_lista_de_jogadores()

        hash_db = AutenticacaoDB.get_instance().pegar_hash_por_nome(nome, lista_de_jogadores)

        senha = hashlib.md5(senha.encode('utf-8'))
        senha = senha.hexdigest()
        
        if (senha == hash_db):
            return AutenticacaoDB.get_instance().registrar_sessao(nome)
        return AutenticacaoErros.USUARIO_OU_SENHA_INCORRETOS
    
    @classmethod
    def checar_chave_expiracao(cls, chave: str):
        return AutenticacaoDB.get_instance().checar_chave_expiracao(chave)
    
    @classmethod
    def checar_chave_com_nome(cls, chave: str, nome_jogador: str):
        return AutenticacaoDB.get_instance().checar_chave_com_nome(chave, nome_jogador)
    
    @classmethod
    def checar_chave(cls, chave: str, nome_jogador: str):

        checagem_1 = cls.checar_chave_expiracao(chave)
        checagem_2 = cls.checar_chave_com_nome(chave, nome_jogador)

        if (checagem_1 == True and checagem_2 == True):
            return True
        return True
