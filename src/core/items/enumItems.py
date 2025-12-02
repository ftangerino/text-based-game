from enum import Enum

class EnumItems(Enum):
    CIMITARRA = ("Cimitarra", 1, 0, 0, 0, 0, 0, 0, 0)


    def __init__(self, nome, nivel, hp, mp, str, dex, int, def_, luk):
        self.nome = nome
        self.nivel = nivel
        self.hp = hp
        self.mp = mp
        self.str = str
        self.dex = dex
        self.int = int
        self.def_ = def_
        self.luk = luk
    