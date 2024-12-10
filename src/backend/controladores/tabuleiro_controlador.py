from modelos.tabuleiro import Tabuleiro
from controladores.embarcacao_controlador import EmbarcacoesControlador

# Controlador do tabuleiro
class TabuleiroControlador():

    # ========================== Controlar área da parte do tabuleiro

    @classmethod
    def pegar_tabuleiro_por_parte(cls, tabuleiro: Tabuleiro, parte_tabuleiro: str):
        tabuleiro_parte = tabuleiro.devolver_tabuleiro_por_parte(parte_tabuleiro)
        representacao = []
        for linha in tabuleiro_parte:
           representacao.append(''.join(linha)) 
        return representacao
    
    @classmethod
    def pegar_tabuleiro_camuflado_por_parte(cls, tabuleiro: Tabuleiro, parte_tabuleiro: str):
        tabuleiro_parte = tabuleiro.devolver_tabuleiro_camuflado_por_parte(parte_tabuleiro)
        representacao = []
        for linha in tabuleiro_parte:
           representacao.append(''.join(linha)) 
        return representacao
    
    # ========================== Controlar peças no tabuleiro
    
    # ========== Embarcações para colocar

    @classmethod
    def definir_embarcacoes_para_colocar(cls, tabuleiro: Tabuleiro):
        lista : list = EmbarcacoesControlador.criar_embarcacoes()
        tabuleiro.definir_embarcacoes_tabuleiro(lista)
    
    @classmethod
    def listar_embarcacoes_para_colocar(cls, tabuleiro: Tabuleiro, parte_tabuleiro: str):
        return tabuleiro.delvover_embarcacoes_para_colocar(parte_tabuleiro)
    
    @classmethod
    def pegar_embarcacao_para_colocar_por_nome(cls, tabuleiro: Tabuleiro, parte_tabuleiro: str, nome_embarcacao: str):
        embarcacoes_para_colocar = cls.listar_embarcacoes_para_colocar(tabuleiro, parte_tabuleiro)
        embarcacao = None

        for e in embarcacoes_para_colocar:
            if e._nome == nome_embarcacao:
                embarcacao = e

        if (embarcacao != None):
            return embarcacao
        return False
    
    @classmethod 
    def remover_embarcacao_da_lista_colocar(cls, tabuleiro: Tabuleiro, parte_tabuleiro: str, embarcacao: object):
        tabuleiro.remover_embarcacao_para_colocar_da_parte(parte_tabuleiro, embarcacao)

    # ========== Embarcações para vivas
    
    @classmethod
    def definir_embarcacao_viva_na_parte(cls, tabuleiro: Tabuleiro, parte_tabuleiro: str, embarcacao: object):
        tabuleiro.definir_embarcacao_viva_na_parte(parte_tabuleiro, embarcacao)

    @classmethod
    def listar_embarcacoes_vivas(cls, tabuleiro: Tabuleiro, parte_tabuleiro: str):
        return tabuleiro.delvover_embarcacoes_vivas(parte_tabuleiro)

    @classmethod 
    def remover_embarcacao_da_lista_viva(cls, tabuleiro: Tabuleiro, parte_tabuleiro: str, embarcacao: object):
        tabuleiro.remover_embarcacao_viva(parte_tabuleiro, embarcacao)

    # ========== Mudanças na área com as embarcações
        
    # Colocando embarcacoes no tabuleiro             
    @classmethod
    def colocar_embarcacoes_no_tabuleiro(cls, tabuleiro: Tabuleiro, parte_tabuleiro: str, nome_embarcacao: str, coord_x: str, coord_y: int, orientacao: str):

        embarcacao = cls.pegar_embarcacao_para_colocar_por_nome(tabuleiro, parte_tabuleiro, nome_embarcacao)
        if embarcacao == False:
            return False

        checar_posicionamento = tabuleiro.colocar_embarcacao_na_parte(parte_tabuleiro, embarcacao, coord_x, coord_y, orientacao)

        if checar_posicionamento == True:
            cls.definir_embarcacao_viva_na_parte(tabuleiro, parte_tabuleiro, embarcacao)
            cls.remover_embarcacao_da_lista_colocar(tabuleiro, parte_tabuleiro, embarcacao)
            return {"message": "Peça colocada"}
        else:
            return {"message": "Falha em colocar peça"}
        
    # ========== Ações no tabuleiro
    
    @classmethod
    def disparo(cls, tabuleiro: Tabuleiro, parte_tabuleiro: str, coord_x: str, coord_y: int):
        return tabuleiro.disparo(parte_tabuleiro, coord_x, coord_y)
    
    @classmethod
    def comparar_tabuleiros_por_parte(cls, tabuleiro: Tabuleiro, parte_tabuleiro: str):
        return tabuleiro.comparar_tabuleiros_por_parte(parte_tabuleiro)
        