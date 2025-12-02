import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.jogadores.jogador import Jogador
from core.inimigos.inimigo import Inimigo

class Combate:
    def __init__(self, jogador: Jogador, inimigos: list[Inimigo]):
        self.jogador = jogador
        self.inimigos = inimigos

    def mostrar_status(self):
        print(f"\nStatus do Jogador: {self.jogador.toString()}")
        print("Inimigos:")
        for idx, inimigo in enumerate(self.inimigos, start=1):
            if inimigo.esta_vivo():
                print(f"{idx}. {inimigo.toString()}")

    def atacar_inimigo(self, grupo_inimigos):
        inimigos_vivos = [inimigo for inimigo in grupo_inimigos if inimigo.esta_vivo()]
        for idx, inimigo in enumerate(inimigos_vivos, start=1):
            print(f"{idx}. {inimigo.nome} - HP: {inimigo.hp}")

        escolha = input("Escolha um inimigo para atacar: ")

        if escolha.isdigit():
            escolha = int(escolha)
            if 1 <= escolha <= len(inimigos_vivos):
                inimigo_escolhido = inimigos_vivos[escolha - 1]
                dano = self.jogador.atacar()
                inimigo_escolhido.receber_dano(dano)
                print(f"Você causou {dano} de dano ao {inimigo_escolhido.nome}!")
                if not inimigo_escolhido.esta_vivo():
                    print(f"Você derrotou {inimigo_escolhido.nome}!")
                    grupo_inimigos.remove(inimigo_escolhido)
                return grupo_inimigos
            else:
                print("Escolha inválida, tente novamente.")
        else:
            print("Entrada inválida, tente novamente.")
        return grupo_inimigos

    def inimigos_atacam(self, grupo_inimigos):
        for inimigo in grupo_inimigos:
            if inimigo.esta_vivo():
                dano = inimigo.atacar()
                self.jogador.receber_dano(dano)
                print(f"{inimigo.nome} atacou e causou {dano} de dano!")
                if not self.jogador.esta_vivo():
                    print("Você foi derrotado!")
                    break
