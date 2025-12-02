from enum import Enum


class EnumInimigos(Enum):
    GOBLIN = ("Goblin", 1, 50, 20, 15, 10, 5, 3, 8, "👺", 15)
    URSO = ("Urso", 1, 80, 30, 20, 15, 10, 5, 5, "🐻", 25)
    URUBU = ("Urubu", 1, 50, 20, 15, 10, 5, 3, 8, "🦅", 15)
    DRAGAO = ("Dragao", 1, 100, 100, 30, 20, 10, 10, 10, "🐉", 50)
    ORC = ("Orc", 1, 80, 50, 25, 15, 5, 5, 5, "👹", 30)
    ESQUELETO = ("Esqueleto", 1, 40, 10, 10, 5, 2, 1, 1, "💀", 10)
    ARANHA = ("Aranha", 1, 30, 10, 5, 5, 2, 1, 1, "🕷️", 8)
    LOBISOMEM = ("Lobisomem", 1, 70, 30, 20, 15, 10, 5, 5, "🐺", 28)
    ZUMBI = ("Zumbi", 1, 60, 20, 10, 10, 5, 3, 3, "🧟", 18)
    VAMPIRO = ("Vampiro", 1, 80, 40, 20, 20, 15, 10, 10, "🧛", 35)
    BRUXA = ("Bruxa", 1, 60, 40, 10, 10, 15, 5, 5, "🧙‍♀️", 22)
    DEMONIO = ("Demonio", 1, 120, 80, 40, 30, 20, 15, 15, "👿", 60)
    DIABO = ("Diabo", 1, 150, 100, 50, 40, 30, 20, 20, "😈", 70)
    LICH = ("Lich", 1, 200, 150, 60, 50, 40, 30, 30, "☠️", 80)

    def __init__(self, nome, nivel, hp, mp, str, dex, int, def_, luk, icone, experiencia):
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
        self.experiencia = experiencia
