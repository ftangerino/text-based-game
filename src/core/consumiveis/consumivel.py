from ..entidade import Entidade
from uuid import uuid4
from enum import Enum
import random
#oi
class Consumivel:
    def __init__(self, nome, hp, mp):
        self.nome = nome
        self.hp = hp
        self.mp = mp