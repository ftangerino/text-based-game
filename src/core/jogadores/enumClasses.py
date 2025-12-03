from enum import Enum


class EnumClasses(Enum):
            #      nome      nv  hp   mp str dex  int def luk  icone
    GUERREIRO = ("Guerreiro", 1, 100, 50, 30, 20, 10, 12, 5, "⚔️")
    MAGO      = ("Mago",      1, 50, 120, 10, 10, 30, 8, 10, "🧙")
    ARQUEIRO  = ("Arqueiro",  1, 80, 80,  18, 28, 18, 10, 15, "🏹")

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
