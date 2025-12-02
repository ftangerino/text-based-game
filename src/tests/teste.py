import json
import os
import random
import sys
from datetime import datetime
from typing import Dict, List

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.inimigos.enumInimigos import EnumInimigos
from core.jogadores.enumClasses import EnumClasses
from core.jogadores.jogador import Jogador
from core.mapa.mapa import Mapa

LINHAS = 5
COLUNAS = 5


def solicitar_nome() -> str:
    while True:
        nome = input("Digite o nome do seu personagem: ").strip()
        if nome:
            return nome
        print("O nome não pode ser vazio. Tente novamente.")


def escolher_classe() -> EnumClasses:
    print("Escolha uma classe:")
    for idx, classe in enumerate(EnumClasses, start=1):
        print(f"{idx}. {classe.nome}")

    while True:
        escolha = input("Digite o número da classe desejada: ")
        if escolha.isdigit():
            indice = int(escolha) - 1
            if 0 <= indice < len(EnumClasses):
                return list(EnumClasses)[indice]
        print("Classe inválida, tente novamente.")


def criar_jogador(nome: str, classe: EnumClasses, mapa: Mapa) -> Jogador:
    jogador = Jogador(
        nome=nome,
        nivel=classe.nivel,
        hp=classe.hp,
        mp=classe.mp,
        str=classe.str,
        dex=classe.dex,
        int=classe.int,
        def_=classe.def_,
        luk=classe.luk,
        mapa=mapa,
        posicao_inicial=(0, 0),
    )
    jogador.setVida(classe.hp)
    return jogador


def gerar_inimigos_fase(configuracao: Dict[EnumInimigos, int], mapa: Mapa) -> List[EnumInimigos]:
    inimigos = []
    for tipo, quantidade in configuracao.items():
        inimigos.extend([tipo for _ in range(quantidade)])

    random.shuffle(inimigos)

    for inimigo in inimigos:
        while True:
            x, y = random.randint(0, LINHAS - 1), random.randint(0, COLUNAS - 1)
            if mapa.obter_posicao(x, y) == ".":
                mapa.adicionar_inimigo(x, y, inimigo)
                break

    return inimigos


def registrar_pontuacao(nome: str, classe: EnumClasses, pontos: int) -> None:
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)
    placar_path = os.path.join(data_dir, "scores.json")

    registro = {
        "horario": datetime.now().isoformat(timespec="seconds"),
        "nome": nome,
        "classe": classe.nome,
        "pontos": pontos,
    }

    try:
        with open(placar_path, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        dados = []

    dados.append(registro)

    with open(placar_path, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)


def jogar_fase(jogador: Jogador, mapa: Mapa, inimigos: List[EnumInimigos], nome_fase: str, pontos: int) -> int:
    print(f"\nIniciando {nome_fase}! Derrote todos os inimigos para avançar.")
    mapa.exibir_mapa()

    while inimigos:
        jogador.mover_jogador_mapa()

        posicao_jogador = jogador.posicao
        if posicao_jogador in mapa.inimigos:
            inimigo_encontrado = mapa.inimigos[posicao_jogador]
            print(f"Você encontrou um {inimigo_encontrado.nome}!")

            while True:
                escolha = input("Digite 1 para atacar ou 'sair' para fugir: ")
                if escolha.lower() == "sair":
                    print("Você decidiu fugir da batalha!")
                    break

                if escolha == "1":
                    mapa.remover_inimigo(*posicao_jogador)
                    inimigos.remove(inimigo_encontrado)
                    pontos += 10
                    print(f"Você derrotou o {inimigo_encontrado.nome}! Pontos atuais: {pontos}")
                    break

                print("Escolha inválida, tente novamente.")

    print(f"Você completou {nome_fase}!")
    return pontos + 20


def main():
    nome = solicitar_nome()
    classe_escolhida = escolher_classe()

    fases = [
        {
            "nome": "Fase 1 - Floresta Nebulosa",
            "inimigos": {EnumInimigos.GOBLIN: 2, EnumInimigos.ZUMBI: 1},
        },
        {
            "nome": "Fase 2 - Grutas Escuras",
            "inimigos": {EnumInimigos.ORC: 2, EnumInimigos.GOBLIN: 1},
        },
        {
            "nome": "Fase 3 - Ruínas Antigas",
            "inimigos": {EnumInimigos.URSO: 1, EnumInimigos.ORC: 1, EnumInimigos.ZUMBI: 1},
        },
    ]

    mapa = Mapa(LINHAS, COLUNAS)
    jogador = criar_jogador(nome, classe_escolhida, mapa)

    pontos = 0
    for fase in fases:
        mapa = Mapa(LINHAS, COLUNAS)
        jogador.mapa = mapa
        jogador.posicao = (0, 0)
        mapa.atualizar_posicao(*jogador.posicao, "❤")

        inimigos = gerar_inimigos_fase(fase["inimigos"], mapa)
        pontos = jogar_fase(jogador, mapa, inimigos, fase["nome"], pontos)

    print(f"Parabéns, {nome}! Você concluiu todas as fases com {pontos} pontos.")
    registrar_pontuacao(nome, classe_escolhida, pontos)


if __name__ == "__main__":
    main()
