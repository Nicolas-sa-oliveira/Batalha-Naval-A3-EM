from src.backend.modelos.partida import Partida

# DB das partidas aplicando singleton.
class PartidaDB():

    _instance = None
    _lista_de_partidas : list = []

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = PartidaDB()
        return cls._instance
    
    @classmethod
    def listar_partidas(cls):
        return cls.get_instance()._lista_de_partidas
    
    @classmethod
    def terminar_partida_por_id(cls, id: int):
        cls.get_instance().atualizar_status_por_id(id, "terminada")
        # cls.get_instance()._lista_de_partidas = [p for p in  cls.get_instance()._lista_de_partidas if p._id != id]
    
    @classmethod
    def checar_jogador_em_partida(cls, nome_jogador: str):
        lista_de_partidas = cls.get_instance().listar_partidas()

        for partida in lista_de_partidas:
            if partida._jogador_a["nome"] == nome_jogador or partida._jogador_b["nome"] == nome_jogador:
                return {"message": f"Partida iniciada no id: {partida._id}"}
        return {"message": "Você não está em fila e nem em uma partida"}
    
    @classmethod
    def começar_nova_partida(cls, jogador_a: object, jogador_b: object):
        partida : Partida = Partida(jogador_a, jogador_b)
        cls.get_instance()._lista_de_partidas.append(partida)

    @classmethod
    def pegar_id_por_jogador(cls, jogador_a: object):
        lista_de_partidas = cls.get_instance().listar_partidas()
        id = 0

        for partida in lista_de_partidas:
            if partida._jogador_a == jogador_a:
                id = partida._id
        
        return id
    
    @classmethod
    def pegar_nome_jogador_por_id(cls, id: int, id_jogador: str):
        lista_de_partidas = cls.get_instance().listar_partidas()

        for partida in lista_de_partidas:
            if partida._id == id:
                if id_jogador == "a":
                    return partida._jogador_a["nome"]
                elif id_jogador == "b": 
                    return partida._jogador_b["nome"]
                else:
                    return False
    
    @classmethod
    def pegar_tabuleiro_por_id(cls, id: int):
        lista_de_partidas = cls.get_instance().listar_partidas()
        tabuleiro = None

        for partida in lista_de_partidas:
            if partida._id == id:
                tabuleiro = partida._tabuleiro
        
        return tabuleiro
    
    @classmethod
    def pegar_status_por_id(cls, id: int):
        lista_de_partidas = cls.get_instance().listar_partidas()
        status = ""

        for partida in lista_de_partidas:
            if partida._id == id:
                status = partida._status
        
        return status
    
    @classmethod 
    def atualizar_status_por_id(cls, id: int, novo_status: str):
        lista_de_partidas = cls.get_instance().listar_partidas()

        for partida in lista_de_partidas:
            if partida._id == id:
                partida._status = novo_status

    @classmethod
    def pegar_turno_por_id(cls, id: int):
        lista_de_partidas = cls.get_instance().listar_partidas()
        turno = 0

        for partida in lista_de_partidas:
            if partida._id == id:
                turno = partida._turno
        
        return turno
    
    @classmethod
    def passar_turno(cls, id: int):
        lista_de_partidas = cls.get_instance().listar_partidas()

        for partida in lista_de_partidas:
            if partida._id == id:
                partida._turno += 1

    @classmethod
    def pegar_repeticoes_por_id(cls, id: int):
        lista_de_partidas = cls.get_instance().listar_partidas()
        repeticoes = 0

        for partida in lista_de_partidas:
            if partida._id == id:
                repeticoes = partida._repeticoes_jogadas
        
        return repeticoes
    
    @classmethod
    def atualizar_repeticao_por_id(cls, id: int):
        lista_de_partidas = cls.get_instance().listar_partidas()

        for partida in lista_de_partidas:
            if partida._id == id:
                partida._repeticoes_jogadas += 1
                if partida._repeticoes_jogadas == 3:
                    partida._repeticoes_jogadas = 0