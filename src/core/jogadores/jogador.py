# /src/core/jogador.py

from ..entidade import Entidade

class Jogador(Entidade):
    def __init__(self, nome, nivel, hp, mp, str, dex, int, def_, luk):
        super().__init__(0, nome, nivel, hp, mp, str, dex, int, def_, luk)
        self.consumiveis = []
        self.items = []
        self.hp = hp
        self.vida_maxima = hp

    def setVida(self, vida_atual):
        if vida_atual > self.vida_maxima:
            self.hp = self.vida_maxima
        else:
            self.hp = vida_atual
        
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

    def mover(self):
        esquerda = "esquerda"
        direita = "direita"
        cima = "cima"
        descansar = "descansar"
        count = 0
        while True:
            count += 1
            if count == 100:
                break
            print("""
                Onde você deseja ir?
                    Esquerda: 1
                    Direita: 2
                    Cima: 3
                """ )
            print(direcao := str(input("Digite a direção: ")))
            if direcao == esquerda or direcao == direita or direcao == cima:
                print(f"Você foi para {direcao}")
                break
            elif direcao == descansar: 
                cura = self.hp * 0.1
                self.setVida(self.hp + cura)
                print(f"Você descansou e recuperou {cura} de vida")
            else: print("Direção inválida")


