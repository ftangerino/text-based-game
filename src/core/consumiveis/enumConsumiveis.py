from enum import Enum

class EnumConsumiveis(Enum):
    POCAO_DE_VIDA = ("Poção de Vida", 50, 0)
    POCAO_DE_MANA = ("Poção de Mana", 0, 50)
    PAO = ("Pão", 10, 0)
    QUEIJO = ("Queijo", 10, 0)
    TORTA = ("Torta", 10, 0)

    def __init__(self, nome, hp, mp):
        self.nome = nome
        self.hp = hp
        self.mp = mp