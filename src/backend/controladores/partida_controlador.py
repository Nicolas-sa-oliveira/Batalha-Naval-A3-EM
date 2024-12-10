from persistencia.partida_db import PartidaDB
from controladores.tabuleiro_controlador import TabuleiroControlador
from controladores.jogador_controlador import JogadorControlador

# Controlador da partida.
class PartidaControlador:

    @classmethod
    def começar_nova_partida(cls, jogador_a: object, jogador_b: object):
        PartidaDB().get_instance().começar_nova_partida(jogador_a, jogador_b)
        id = cls.pegar_id_por_jogador(jogador_a)
        tabuleiro = cls.pegar_tabuleiro_por_id(id)
        TabuleiroControlador.definir_embarcacoes_para_colocar(tabuleiro)

    @classmethod
    def listar_partidas(cls):
        return PartidaDB().get_instance().listar_partidas
    
    @classmethod
    def terminar_partida_por_id(cls, id: int):
        return PartidaDB().get_instance().terminar_partida_por_id(id)
    
    @classmethod
    def checar_jogador_em_partida(cls, nome_jogador: str):
        return PartidaDB().get_instance().checar_jogador_em_partida(nome_jogador)

    @classmethod
    def pegar_id_por_jogador(cls, jogador_a: object):
        return PartidaDB.get_instance().pegar_id_por_jogador(jogador_a)
    
    @classmethod
    def pegar_tabuleiro_por_id(cls, id: int):
        return PartidaDB.get_instance().pegar_tabuleiro_por_id(id)
    
    @classmethod
    def pegar_nome_jogador_por_id(cls, id: int, id_jogador: str):
        return PartidaDB.get_instance().pegar_nome_jogador_por_id(id, id_jogador)
    
    @classmethod
    def pegar_status_por_id(cls, id: int):
        return PartidaDB.get_instance().pegar_status_por_id(id)

    @classmethod 
    def atualizar_status_por_id(cls, id: int, novo_status: str):
        return PartidaDB.get_instance().atualizar_status_por_id(id, novo_status)

    @classmethod
    def pegar_turno_por_id(cls, id: int):
        return PartidaDB.get_instance().pegar_turno_por_id(id)
    
    @classmethod
    def passar_turno(cls, id: int):
        cls.checar_fim_do_jogo(id)
        return PartidaDB.get_instance().passar_turno(id)
    
    @classmethod
    def pegar_repeticoes_por_id(cls, id: int):
        return PartidaDB.get_instance().pegar_repeticoes_por_id(id)
    
    @classmethod
    def atualizar_repeticoes_por_id(cls, id: int):
        return PartidaDB.get_instance().atualizar_repeticao_por_id(id)

    @classmethod
    def pegar_representacao_tabuleiro_partida(cls, id: int, nome_jogador: str):
        tabuleiro = cls.pegar_tabuleiro_por_id(id)

        rep_list = []

        jogador_a = cls.pegar_nome_jogador_por_id(id, "a")
        jogador_b = cls.pegar_nome_jogador_por_id(id, "b")

        if (jogador_a == nome_jogador):
            rep_tabuleiro = TabuleiroControlador.pegar_tabuleiro_por_parte(tabuleiro, "a")
            rep_camuflado = TabuleiroControlador.pegar_tabuleiro_camuflado_por_parte(tabuleiro, "b")
        elif (jogador_b == nome_jogador):
            rep_tabuleiro = TabuleiroControlador.pegar_tabuleiro_por_parte(tabuleiro, "b")
            rep_camuflado = TabuleiroControlador.pegar_tabuleiro_camuflado_por_parte(tabuleiro, "a")
        else: 
            return {"message": "Jogador não pertence ao jogo"}
        
        rep_list.append(rep_tabuleiro)
        rep_list.append(rep_camuflado)

        return rep_list
    
    @classmethod
    def checar_embarcacoes_disponiveis(cls, id: int, nome_jogador: str):
        tabuleiro = cls.pegar_tabuleiro_por_id(id)
        jogador_a = cls.pegar_nome_jogador_por_id(id, "a")
        jogador_b = cls.pegar_nome_jogador_por_id(id, "b")

        if (jogador_a == nome_jogador):
            return TabuleiroControlador.listar_embarcacoes_para_colocar(tabuleiro, "a")
        elif (jogador_b == nome_jogador):
            return TabuleiroControlador.listar_embarcacoes_para_colocar(tabuleiro, "b")
        else: 
            return {"message": "Jogador não pertence ao jogo"}
        
    @classmethod
    def colocar_embarcacao_tabuleiro(cls, id: int, nome_jogador: str, embarcao: str, coord_x: str, coord_y: int, orientacao: str):
        tabuleiro = cls.pegar_tabuleiro_por_id(id)

        jogador_a = cls.pegar_nome_jogador_por_id(id, "a")
        jogador_b = cls.pegar_nome_jogador_por_id(id, "b")

        checar_colocacao = None
        checar_fim_prep = None

        if (jogador_a == nome_jogador):
            checar_colocacao = TabuleiroControlador.colocar_embarcacoes_no_tabuleiro(tabuleiro, "a", embarcao, coord_x, coord_y, orientacao)
            checar_fim_prep = cls.checar_fim_preparacao(tabuleiro)
            if checar_fim_prep == True : cls.passar_para_fase_de_embate(id)
            return checar_colocacao
        elif (jogador_b == nome_jogador):
            checar_colocacao = TabuleiroControlador.colocar_embarcacoes_no_tabuleiro(tabuleiro, "b", embarcao, coord_x, coord_y, orientacao)
            checar_fim_prep = cls.checar_fim_preparacao(tabuleiro)
            if checar_fim_prep == True : cls.passar_para_fase_de_embate(id)
            return checar_colocacao
        else: 
            return {"message": "Jogador não pertence ao jogo"}
        
    @classmethod
    def checar_fim_preparacao(cls, tabuleiro: object):
        lista_total = []
        lista_a = TabuleiroControlador.listar_embarcacoes_para_colocar(tabuleiro, "a")
        lista_b = TabuleiroControlador.listar_embarcacoes_para_colocar(tabuleiro, "b")
        
        lista_total.append(lista_a)
        lista_total.append(lista_b)
        
        if lista_total == [[], []]:
            return True
        return False
    
    @classmethod
    def passar_para_fase_de_embate(cls, id):
        cls.atualizar_status_por_id(id, "embate")

    @classmethod
    def realizar_disparo(cls, id: int, nome_jogador: str, coord_x: str, coord_y: int):
        tabuleiro = cls.pegar_tabuleiro_por_id(id)
        jogador_a = cls.pegar_nome_jogador_por_id(id, "a")
        jogador_b = cls.pegar_nome_jogador_por_id(id, "b")
        status = cls.pegar_status_por_id(id)
        turno = cls.pegar_turno_por_id(id)
        repeticoes = cls.pegar_repeticoes_por_id(id)
        resultado : bool

        if (jogador_a == nome_jogador and status == "embate"):
            if (turno % 2 != 0):
                resultado = TabuleiroControlador.disparo(tabuleiro, "b", coord_x, coord_y)
                if resultado == True:
                    if repeticoes < 2:
                        cls.atualizar_repeticoes_por_id(id)
                        return {"message": "Embarcação Encontrada!"}
                    cls.atualizar_repeticoes_por_id(id)
                    cls.passar_turno(id)
                    return {"message": "Embarcação Encontrada!"}
                else:
                    cls.passar_turno(id)
                    return {"message": "Tiro na água!"}
            else:
                return  {"message": "Não é seu turno ainda"}
        elif (jogador_b == nome_jogador and status == "embate"):
            if (turno % 2 == 0):
                resultado = TabuleiroControlador.disparo(tabuleiro, "a", coord_x, coord_y)
                if resultado == True:
                    if repeticoes < 3:
                        cls.atualizar_repeticoes_por_id(id)
                        return {"message": "Embarcação Encontrada!"}
                    cls.atualizar_repeticoes_por_id(id)
                    cls.passar_turno(id)
                    return {"message": "Embarcação Encontrada!"}
                else:
                    cls.passar_turno(id)
                    return {"message": "Tiro na água!"}
            else:
                return  {"message": "Não é seu turno ainda"}
        elif (jogador_a != nome_jogador and jogador_b != nome_jogador): 
            return {"message": "Jogador não pertence ao jogo"}
        elif (status == "terminada"):

            tabuleiro = cls.pegar_tabuleiro_por_id(id)
            checagem_a = TabuleiroControlador.comparar_tabuleiros_por_parte(tabuleiro, "a")
            checagem_b = TabuleiroControlador.comparar_tabuleiros_por_parte(tabuleiro, "b")

            if checagem_a == True:
                return {"message": "A partida foi encerrada. O vencedor é {}".format(jogador_b)}
            elif checagem_b == True:
                return {"message": "A partida foi encerrada. O vencedor é {}".format(jogador_a)}
        
        return {"message": "Você não pode realizar disparos na fase de preparação"}

    @classmethod    
    def checar_fim_do_jogo(cls, id: int):
        tabuleiro = cls.pegar_tabuleiro_por_id(id)
        checagem_a = TabuleiroControlador.comparar_tabuleiros_por_parte(tabuleiro, "a")
        checagem_b = TabuleiroControlador.comparar_tabuleiros_por_parte(tabuleiro, "b")

        if checagem_a == True:
            cls.finalizar_jogo(id, "b")
        elif checagem_b == True:
            cls.finalizar_jogo(id, "a")

    @classmethod
    def finalizar_jogo(cls, id: int, vencedor: str):
        JogadorControlador.aumentar_pontuacao_por_nome(vencedor)
        cls.terminar_partida_por_id(id)
