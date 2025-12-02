import sys
import os
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.jogadores.jogador import Jogador
from core.inimigos.inimigo import Inimigo
from core.inimigos.enumInimigos import EnumInimigos
from collections import Counter
from core.mapa.mapa import Mapa

linhas = 5
colunas = 5
mapa = Mapa(linhas, colunas)

jogador = Jogador(
    nome="Herooii", 
    nivel=1, 
    hp=120, 
    mp=50, 
    str=20, 
    dex=15, 
    int=10, 
    def_=5, 
    luk=12, 
    mapa=mapa, 
    posicao_inicial=(0, 0)
)
jogador.setVida(120)


tipos_inimigos = [EnumInimigos.GOBLIN, EnumInimigos.ZUMBI, EnumInimigos.URSO, EnumInimigos.ORC]
peso_inimigos = {
    EnumInimigos.GOBLIN: 0.4,
    EnumInimigos.ZUMBI: 0.4,
    EnumInimigos.URSO: 0.2,
    EnumInimigos.ORC: 0.1
}

inimigos_aleatorios = random.choices(tipos_inimigos, weights=peso_inimigos.values(), k=10)
inimigos_aleatorios_movimento = random.choices(tipos_inimigos, weights=peso_inimigos.values(), k=3)
contagem_inimigos = Counter(inimigos_aleatorios)


for inimigo in inimigos_aleatorios:
    while True:
        x, y = random.randint(0, linhas - 1), random.randint(0, colunas - 1)
        if mapa.obter_posicao(x, y) == ".":
            mapa.adicionar_inimigo(x, y, inimigo)
            break

# mapa.exibir_mapa()

# Loop principal do jogo
while inimigos_aleatorios:
    jogador.mover_jogador_mapa()
    
    # encontros
    pos_jogador = jogador.posicao
    if pos_jogador in mapa.inimigos:
        inimigo_encontrado = mapa.inimigos[pos_jogador]
        print(f"Você encontrou um {inimigo_encontrado.name}!")

        # batalha
        grupo_inimigos = [inimigo_encontrado]
        while grupo_inimigos:
            print("\nInimigos à frente:")
            for idx, inimigo in enumerate(grupo_inimigos, start=1):
                print(f"{idx}. {inimigo.name}")

            escolha = input("Escolha um inimigo para atacar (1) ou 'sair' para fugir: ")

            if escolha.lower() == "sair":
                print("Você decidiu fugir da batalha!")
                break

            if escolha.isdigit():
                escolha = int(escolha)
                if 1 <= escolha <= len(grupo_inimigos):
                    inimigo_atacado = grupo_inimigos.pop(escolha - 1)
                    print(f"Você atacou o {inimigo_atacado.name}!")
                    mapa.remover_inimigo(*pos_jogador)  # Remova o inimigo do mapa
                    inimigos_aleatorios.remove(inimigo_atacado)
                    if not grupo_inimigos:
                        print("Você derrotou todos os inimigos deste grupo!")
                        break
                else:
                    print("Escolha inválida, tente novamente.")
            else:
                print("Entrada inválida, tente novamente.")
    
    # mapa.exibir_mapa()

print("Você derrotou todos os inimigos e completou o desafio!")