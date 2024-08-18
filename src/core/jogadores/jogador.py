# /src/core/jogador.py

from ..entidade import Entidade

class Jogador(Entidade):
    def __init__(self, nome, nivel, hp, mp, str, dex, int, def_, luk):
        super().__init__(0, nome, nivel, hp, mp, str, dex, int, def_, luk)
        self.consumiveis = []
        self.items = []
    
    def pegarConsumivel(self, consumivel):
        self.consumiveis.append(consumivel)

    def usarConsumivel(self, consumivel):
        self.hp += consumivel.hp
        self.mp += consumivel.mp

    def mostrarConsumivel(self):
        consumiveis_to_dict = {}
        for consumivel in self.consumiveis:
            if consumivel.nome in consumiveis_to_dict:
                consumiveis_to_dict[consumivel.nome] += 1
            else:  
                consumiveis_to_dict[consumivel.nome] = 1

        todosItems = ["Items:\n"]
        for nome, quantidade in consumiveis_to_dict.items():
            todosItems.append(f"{nome}: {quantidade}")

        playerItems = "\n".join(todosItems)
        print(playerItems)