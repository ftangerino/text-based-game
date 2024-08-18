# /src/core/entidade.py

class Entidade:
    def __init__(self, id, nome, nivel, hp, mp, str, dex, int, def_, luk):
        self.id = id
        self.nome = nome
        self.nivel = nivel
        self.hp = hp
        self.mp = mp
        self.str = str
        self.dex = dex
        self.int = int
        self.def_ = def_
        self.luk = luk

    def toString(self):
        return f"Nome: {self.nome} Nivel: {self.nivel}\nHP: {self.hp}\nMP: {self.mp}\nSTR: {self.str}\nDEX: {self.dex}\nINT: {self.int}\nDEF: {self.def_}\nLUK: {self.luk}"