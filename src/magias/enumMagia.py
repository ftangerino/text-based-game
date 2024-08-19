from enum import Enum

class enumMagia(Enum):
    RAIO = ("Raio", 10, 10)
    FOGO = ("Fogo", 20, 20)
    GELO = ("Gelo", 30, 30)

    def __init__(self, nome, dano, custo):
        self.nome = nome
        self.dano = dano
        self.custo = custo
