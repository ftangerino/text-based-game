from enum import Enum


class EnumClasses(Enum):
    # Note o emoji no final da tupla
    GUERREIRO = ("Guerreiro", 1, 100, 50, 30, 20, 10, 10, 5, "⚔️")
    MAGO = ("Mago", 1, 50, 100, 10, 10, 30, 5, 10, "🧙")

    def __init__(self, nome, nivel, hp, mp, str, dex, int, def_, luk, icone):
        self.nome = nome
        self.nivel = nivel
        self.hp = hp
        self.mp = mp
        self.str = str
        self.dex = dex
        self.int = int
        self.def_ = def_
        self.luk = luk
        self.icone = icone
