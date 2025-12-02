from enum import Enum

from .magia import Magia


class enumTecnica(Enum):
    CORTE_PRECISO = ("Corte Preciso", 12, 0, 1)
    GOLPE_ESCUDO = ("Golpe de Escudo", 18, 6, 2)
    LAMINA_TEMPESTUOSA = ("Lâmina Tempestuosa", 26, 10, 3)
    FURIA_DO_GUERREIRO = ("Fúria do Guerreiro", 38, 14, 5)

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
            atributo_base="str",
            tipo="tecnica",
        )
