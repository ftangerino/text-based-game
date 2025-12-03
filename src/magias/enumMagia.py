from enum import Enum

from .magia import Magia


class enumMagia(Enum):
    RAIO = ("Raio", 12, 6, 1)
    FOGO = ("Bola de Fogo", 21, 12, 2)
    GELO = ("Lança de Gelo", 30, 16, 3)
    TEMPESTADE = ("Tempestade Arcana", 45, 22, 5)

    def __init__(self, nome, dano, custo, nivel_requerido):
        self.nome = nome
        self.dano = dano
        self.custo = custo
        self.nivel_requerido = nivel_requerido

    def criar_magia(self):
        return Magia(
            nome=self.nome,
            dano=self.dano,
            custo=self.custo,
            nivel_requerido=self.nivel_requerido,
            atributo_base="int",
            tipo="magia",
        )
