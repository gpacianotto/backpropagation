
from enum import Enum, auto

class TipoCondicaoParada(Enum):
    ERRO_MAXIMO = auto()
    NUM_INTERACOES = auto()

class CondicaoParada():
    def __init__(self, tipo:TipoCondicaoParada,  value:int|float):
        self.tipo:TipoCondicaoParada = tipo
        if self.tipo == TipoCondicaoParada.ERRO_MAXIMO and not isinstance(value, float):
            raise Exception("Valor deve ser float")
        elif self.tipo == TipoCondicaoParada.NUM_INTERACOES and not isinstance(value, int):
            raise Exception("Valor deve ser inteiro")
        self.value = value
        pass
