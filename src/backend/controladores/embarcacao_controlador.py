from modelos.embarcacao import FabricaEmbarcacao

# Controlador de embarcações
class EmbarcacoesControlador():
    
    @classmethod
    def criar_embarcacoes(cls):
        embarcacoes = [
            FabricaEmbarcacao.instance().fabrica('Submarino'),
            FabricaEmbarcacao.instance().fabrica('Submarino'),
            # FabricaEmbarcacao.instance().fabrica('Submarino'),
            FabricaEmbarcacao.instance().fabrica('Navio Pequeno'),
            # FabricaEmbarcacao.instance().fabrica('Navio Pequeno'),
            FabricaEmbarcacao.instance().fabrica('Navio Médio'),
            # FabricaEmbarcacao.instance().fabrica('Navio Grande'),
            FabricaEmbarcacao.instance().fabrica('Porta Aviões')
        ]
        return embarcacoes