import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.jogadores.jogador import Jogador
from core.inimigos.inimigo import Inimigo
from core.inimigos.enum_inimigos import EnumInimigos
from core.consumiveis.consumivel import Consumivel
from core.consumiveis.enumConsumiveis import EnumConsumiveis
import random
import time

jogador = Jogador(nome="Heroi", nivel=1, hp=100, mp=50, str=20, dex=15, int=10, def_=5, luk=12)
todos_consumiveis = [EnumConsumiveis.POCAO_DE_VIDA, EnumConsumiveis.POCAO_DE_MANA, EnumConsumiveis.PAO, EnumConsumiveis.QUEIJO, EnumConsumiveis.TORTA]
count = 0

while True:
    time.sleep(0.5)
    count += 1
    if count == 100:
        break
    if random.randint(1, 1) == 1:
        consumivel = random.choice(todos_consumiveis)
        jogador.pegarConsumivel(Consumivel(nome=consumivel.nome, hp=consumivel.hp, mp=consumivel.mp))
    # print(f"{jogador.mostrarConsumivel()}")
    jogador.mostrarConsumivel()
    print("###################################")

# for i in range(0, 10):
#     if i % 2 == 0:
#         inimigo = EnumInimigos.GOBLIN
#     else:
#         inimigo = EnumInimigos.ZUMBI
#     inimigos.append(Inimigo(=inimigo.nomenome, nivel=inimigo.nivel, hp=inimigo.hp, mp=inimigo.mp, str=inimigo.str, dex=inimigo.dex, int=inimigo.int, def_=inimigo.def_, luk=inimigo.luk))

# for i, inimigo in enumerate(inimigos):
#     if random.randint(1, 5) == 1:
#         inimigo.elite()
#     print(inimigo.toString())



# # jogador = Jogador(nome="Heroi", hp=100, mp=50, str=20, dex=15, int=10, def_=5, luk=12)
# # goblin_arqueiro = Globin()

# # jogador.atacar(goblin_arqueiro, tipo_ataque="fisico")
# # goblin_arqueiro.atacar(jogador)
