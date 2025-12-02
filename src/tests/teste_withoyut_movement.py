import sys
import os
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.jogadores.jogador import Jogador
from core.inimigos.inimigo import Inimigo
from core.inimigos.enumInimigos import EnumInimigos
from collections import Counter
from core.mapa.mapa import Mapa

linhas = 10  # Defina o número de linhas do mapa
colunas = 10  # Defina o número de colunas do mapa
mapa = Mapa(linhas, colunas)

jogador = Jogador(nome="Avello", nivel=1, hp=120, mp=50, str=20, dex=15, int=10, def_=5, luk=12, mapa=mapa, posicao_inicial=(0, 0))
jogador.setVida(120)
# print(jogador.toString())   

tipos_inimigos = [EnumInimigos.GOBLIN, EnumInimigos.ZUMBI, EnumInimigos.URSO, EnumInimigos.ORC]
peso_inimigos = {
    EnumInimigos.GOBLIN: 0.4,
    EnumInimigos.ZUMBI: 0.4,
    EnumInimigos.URSO: 0.2,
    EnumInimigos.ORC: 0.1
}

inimigos_aleatorios = random.choices(tipos_inimigos, weights=peso_inimigos.values(), k=10)

print(inimigos_aleatorios)
inimigos = []
contagem_inimigos = Counter(inimigos_aleatorios)
print(contagem_inimigos)

while inimigos_aleatorios:
    jogador.mover()

    grupo_inimigos = inimigos_aleatorios[:3]
    while grupo_inimigos:
        print("\nInimigos à frente:")
        for idx, inimigo in enumerate(grupo_inimigos, start=1):
            print(f"{idx}. {inimigo.name}")

        escolha = input("Escolha um inimigo para atacar (1-3) ou 'sair' para terminar: ")

        if escolha.lower() == "sair":
            print("Você decidiu fugir da batalha!")
            jogador.mover()

        if escolha.isdigit():
            escolha = int(escolha)
            if 1 <= escolha <= len(grupo_inimigos):
                inimigo_atacado = grupo_inimigos.pop(escolha - 1)
                inimigos_aleatorios.remove(inimigo_atacado)
                print(f"Você atacou o {inimigo_atacado.name}!")
                if not grupo_inimigos:
                    print("Você derrotou todos os inimigos deste grupo!")
                    break
            else:
                print("Escolha inválida, tente novamente.")
        else:
            print("Entrada inválida, tente novamente.")

print("Você derrotou todos os inimigos e completou o desafio!")