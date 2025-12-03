from enum import Enum
from .magia import Magia


class enumTecnicasArqueiro(Enum):
    TIRO_PRECISO      = ("Tiro Preciso",        18,  0, 1)
    TIRO_DUPLO        = ("Tiro Duplo",          24,  6, 2)
    CHUVA_DE_FLECHAS  = ("Chuva de Flechas",    30, 12, 3)
    FLECHA_PERFURANTE = ("Flecha Perfurante",   42, 16, 5)

    def __init__(self, nome, dano, custo, nivel_requerido):
        self.nome = nome
        self.dano = dano
        self.custo = custo
        self.nivel_requerido = nivel_requerido

    def criar_tecnica(self):
        return Magia(
            nome=self.nome,
            dano=self.dano,
            custo=self.custo,
            nivel_requerido=self.nivel_requerido,
            atributo_base="dex",
            tipo="tecnica",
        )
