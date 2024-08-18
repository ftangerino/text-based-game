from ..entidade import Entidade
from uuid import uuid4
from enum import Enum
import random

class Inimigo(Entidade):
    def __init__(self, nome, nivel, hp, mp, str, dex, int, def_, luk):
        id = uuid4()
        super().__init__(id, nome, nivel, hp, mp, str, dex, int, def_, luk)

    def elite(self):
        self.nome = f"Elite {self.nome}"
        self.nivel = self.nivel * 2
        self.hp = self.hp * 2
        self.mp = self.mp * 2
        self.str = self.str * 2
        self.dex = self.dex * 2
        self.int = self.int * 2
        self.def_ = self.def_ * 2
        self.luk = self.luk * 2
