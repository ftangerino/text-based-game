import sys
import os
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.jogadores.jogador import Jogador
from core.inimigos.inimigo import Inimigo
from core.inimigos.enumInimigos import EnumInimigos
from core.combate.combate import Combate
from collections import Counter


# Configuração do jogador
jogador = Jogador(nome="Heroi", nivel=1, hp=120, mp=50, str=20, dex=15, int=10, def_=5, luk=12)
jogador.setVida(120)

# Configuração dos inimigos aleatórios
tipos_inimigos = [EnumInimigos.GOBLIN, EnumInimigos.ZUMBI, EnumInimigos.URSO, EnumInimigos.ORC]
peso_inimigos = {
    EnumInimigos.GOBLIN: 0.4,
    EnumInimigos.ZUMBI: 0.4,
    EnumInimigos.URSO: 0.2,
    EnumInimigos.ORC: 0.1
}

inimigos_aleatorios = random.choices(tipos_inimigos, weights=peso_inimigos.values(), k=10)

print(f"{inimigos_aleatorios}\n")
contagem_inimigos = Counter(inimigos_aleatorios)
print(contagem_inimigos)

inimigos = [Inimigo(tipo.name, *tipo.value[1:]) for tipo in inimigos_aleatorios]

combate = Combate(jogador, inimigos)

while inimigos:
    jogador.mover()

    grupo_inimigos = inimigos[:3]
    combate.mostrar_status()

    while grupo_inimigos:
        print("\nInimigos à frente:")
        for idx, inimigo in enumerate(grupo_inimigos, start=1):
            print(f"{idx}. {inimigo.nome}")

        escolha = input("Escolha um inimigo para atacar (1-3) ou 'sair' para terminar: ")

        if escolha.lower() == "sair":
            print("Você decidiu fugir da batalha!")
            jogador.mover()
            break

        grupo_inimigos = combate.atacar_inimigo(grupo_inimigos)

        if not grupo_inimigos:
            print("Você derrotou todos os inimigos deste grupo!")
            break
        else:
            combate.inimigos_atacam(grupo_inimigos)

    # Remover os inimigos derrotados da lista principal
    inimigos = [inimigo for inimigo in inimigos if inimigo.esta_vivo()]

print("Você derrotou todos os inimigos e completou o desafio!")