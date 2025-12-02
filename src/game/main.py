import sys
import json
import os
import random
from datetime import datetime
from typing import Dict, List, Tuple

# Adiciona o diretório pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.jogadores.jogador import Jogador
from core.inimigos.enumInimigos import EnumInimigos
from core.jogadores.enumClasses import EnumClasses
from core.mapa.mapa import Mapa
from core.mapa.enumEventos import EnumEventos 

# Configurações Globais
LINHAS = 5
COLUNAS = 5

def solicitar_nome() -> str:
    while True:
        nome = input("Digite o nome do seu personagem: ").strip()
        if nome:
            return nome
        print("O nome não pode ser vazio.")

def escolher_classe() -> EnumClasses:
    print("\nEscolha uma classe:")
    for idx, classe in enumerate(EnumClasses, start=1):
        print(f"{idx}. {classe.nome} {classe.icone}")

    while True:
        escolha = input("Digite o número da classe desejada: ")
        if escolha.isdigit():
            indice = int(escolha) - 1
            if 0 <= indice < len(EnumClasses):
                return list(EnumClasses)[indice]
        print("Classe inválida.")

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
    jogador.icone = classe.icone 
    return jogador

def gerar_inimigos_fase(configuracao: Dict[EnumInimigos, int], mapa: Mapa) -> List[EnumInimigos]:
    inimigos = []
    for tipo, quantidade in configuracao.items():
        inimigos.extend([tipo for _ in range(quantidade)])
    random.shuffle(inimigos)

    for inimigo in inimigos:
        while True:
            x, y = random.randint(0, LINHAS - 1), random.randint(0, COLUNAS - 1)
            if (x, y) != (0, 0) and mapa.obter_posicao(x, y) == ".":
                mapa.adicionar_inimigo(x, y, inimigo) 
                break
    return inimigos

def gerar_eventos_fase(quantidade: int, mapa: Mapa) -> Dict[Tuple[int, int], EnumEventos]:
    eventos_ativos = {}
    tipos_eventos = [EnumEventos.FONTE_CURA, EnumEventos.CHARADA, EnumEventos.BAU_TESOURO]
    
    for _ in range(quantidade):
        evento_escolhido = random.choice(tipos_eventos)
        while True:
            x, y = random.randint(0, LINHAS - 1), random.randint(0, COLUNAS - 1)
            if (x, y) != (0, 0) and mapa.obter_posicao(x, y) == "." and (x,y) not in eventos_ativos:
                mapa.atualizar_posicao(x, y, evento_escolhido.icone)
                eventos_ativos[(x, y)] = evento_escolhido
                break
    return eventos_ativos

def resolver_charada() -> bool:
    charadas = [
        ("O que é, o que é? Cai em pé e corre deitado?", "chuva"),
        ("O que é, o que é? Tem cabeça e tem dente, não é bicho e nem é gente?", "alho"),
        ("Quanto mais se tira, maior fica?", "buraco"),
        ("O que sempre está na sua frente, mas você não consegue ver?", "futuro")
    ]
    pergunta, resposta_certa = random.choice(charadas)
    print(f"\n📜 CHARADA: {pergunta}")
    resposta = input("Sua resposta: ").lower().strip()
    return resposta == resposta_certa

def registrar_pontuacao(
    nome: str, classe: EnumClasses, pontos: int, stats: Dict, jogador: Jogador
) -> None:
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)
    placar_path = os.path.join(data_dir, "scores.json")

    tempo_total = (datetime.now() - stats["inicio_jogo"]).total_seconds()

    registro = {
        "horario": datetime.now().isoformat(timespec="seconds"),
        "nome": nome,
        "classe": classe.nome,
        "pontos": pontos,
        "metricas_bi": {
            "tempo_sessao_segundos": int(tempo_total),
            "passos_totais": stats["passos_dados"],
            "descansos_realizados": stats["descansos"], # Nova métrica
            "nivel_final": jogador.nivel,
            "experiencia_total_ganha": stats["experiencia_ganha"],
            "niveis_ganhos": stats["niveis_ganhos"],
            "combate": {
                "inimigos_derrotados": stats["inimigos_derrotados"],
                "fugas": stats["fugas"],
                "criticos_acertados": stats["criticos_acertados"],
                "criticos_sofridos": stats["criticos_sofridos"],
                "desvios": stats["desvios"],
                "falhas_criticas_jogador": stats["falhas_criticas_jogador"],
                "falhas_criticas_inimigos": stats["falhas_criticas_inimigos"],
            },
            "eventos": {
                "baus_abertos": stats["baus_abertos"],
                "fontes_usadas": stats["fontes_usadas"],
                "charadas_acertadas": stats["charadas_acertadas"],
                "charadas_erradas": stats["charadas_erradas"]
            }
        }
    }

    try:
        with open(placar_path, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        dados = []
    dados.append(registro)

    with open(placar_path, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)

    print(f"\n[BI] Dados analíticos salvos em {placar_path}")


def calcular_chance_acerto(atacante_dex: int, defesa_defensor: int, evasao_defensor: int) -> float:
    defesa = (defesa_defensor + evasao_defensor) / 2
    chance = 0.7 + (atacante_dex - defesa) * 0.01
    return max(0.1, min(0.95, chance))


def eh_critico(luk_atacante: int) -> bool:
    chance_critico = min(0.5, 0.05 + luk_atacante / 100)
    return random.random() < chance_critico


def calcular_dano(str_atacante: int, def_defensor: int, critico: bool) -> int:
    dano_base = max(1, str_atacante - def_defensor)
    return dano_base * 2 if critico else dano_base


def executar_batalha(
    jogador: Jogador,
    inimigo: EnumInimigos,
    mapa: Mapa,
    posicao_inimigo: Tuple[int, int],
    posicao_anterior: Tuple[int, int],
    stats: Dict,
) -> Tuple[str, int, int]:
    inimigo_hp = inimigo.hp

    while True:
        print(
            f"\n❤️ {jogador.nome}: {jogador.hp}/{jogador.vida_maxima} | "
            f"{inimigo.icone} {inimigo.nome}: {inimigo_hp}/{inimigo.hp}"
        )
        op = input("[1] Atacar | [Sair] Fugir: ").lower()

        if op == "sair":
            print("🏃 Você fugiu! O inimigo permanece no mapa.")
            stats["fugas"] += 1
            mapa.atualizar_posicao(*posicao_inimigo, "I")
            mapa.atualizar_posicao(*posicao_anterior, jogador.icone)
            jogador.posicao = posicao_anterior
            mapa.exibir_mapa()
            return "fugiu", 0, 0

        if op != "1":
            print("Opção inválida.")
            continue

        falha_critica = random.random() < 0.05
        chance_acerto = calcular_chance_acerto(jogador.dex, inimigo.def_, inimigo.dex)
        rolagem = random.random()

        if falha_critica:
            auto_dano = max(1, jogador.str // 5)
            jogador.hp = max(0, jogador.hp - auto_dano)
            print(f"❌ Falha crítica! Você se machucou e perdeu {auto_dano} de HP.")
            print(f"❤️ HP do jogador: {jogador.hp}/{jogador.vida_maxima}")
            stats["falhas_criticas_jogador"] += 1
        elif rolagem <= chance_acerto:
            critico = eh_critico(jogador.luk)
            dano = calcular_dano(jogador.str, inimigo.def_, critico)
            inimigo_hp = max(0, inimigo_hp - dano)
            mensagem_critico = " (CRÍTICO!)" if critico else ""
            if critico:
                stats["criticos_acertados"] += 1
            print(
                f"🗡️ Você atingiu o {inimigo.nome} causando {dano} de dano"
                f"{mensagem_critico}."
            )
            print(f"💔 HP do {inimigo.nome}: {inimigo_hp}/{inimigo.hp}")
        else:
            print("😬 Você errou o ataque!")

        if inimigo_hp <= 0:
            print("Vitória! Inimigo derrotado. (+10 pontos)")
            stats["inimigos_derrotados"] += 1
            mapa.remover_inimigo(*posicao_inimigo)
            mapa.atualizar_posicao(*posicao_inimigo, jogador.icone)
            return "vitoria", 10, inimigo.experiencia

        falha_critica_inimigo = random.random() < 0.05
        chance_acerto_inimigo = calcular_chance_acerto(inimigo.dex, jogador.def_, jogador.dex)
        rolagem_inimigo = random.random()

        if falha_critica_inimigo:
            auto_dano = max(1, inimigo.str // 5)
            inimigo_hp = max(0, inimigo_hp - auto_dano)
            print(
                f"✅ Falha crítica do inimigo! Ele se machucou e perdeu {auto_dano} de HP."
            )
            print(f"💔 HP do {inimigo.nome}: {inimigo_hp}/{inimigo.hp}")
            stats["falhas_criticas_inimigos"] += 1
        elif rolagem_inimigo <= chance_acerto_inimigo:
            critico_inimigo = eh_critico(inimigo.luk)
            dano_inimigo = calcular_dano(inimigo.str, jogador.def_, critico_inimigo)
            jogador.hp = max(0, jogador.hp - dano_inimigo)
            mensagem_critico = " (CRÍTICO!)" if critico_inimigo else ""
            if critico_inimigo:
                stats["criticos_sofridos"] += 1
            print(
                f"⚔️ {inimigo.nome} atacou e causou {dano_inimigo} de dano"
                f"{mensagem_critico}."
            )
            print(f"❤️ HP do jogador: {jogador.hp}/{jogador.vida_maxima}")
        else:
            print(f"🛡️ Você evitou o golpe do {inimigo.nome}!")
            stats["desvios"] += 1

        if jogador.hp <= 0:
            stats["mortes"] += 1
            print("💀 Você foi derrotado! A batalha terminou.")
            return "derrota", 0, 0

def jogar_fase(
    jogador: Jogador,
    mapa: Mapa,
    inimigos: List[EnumInimigos],
    eventos: Dict,
    nome_fase: str,
    pontos: int,
    stats: Dict,
) -> Tuple[int, bool]:
    print(f"\n=== Iniciando {nome_fase}! ===")
    mapa.exibir_mapa()

    while inimigos:
        posicao_anterior = jogador.posicao
        jogador.mover_jogador_mapa(stats)

        stats["passos_dados"] += 1

        pos_jogador = jogador.posicao

        # --- Lógica de Inimigos ---
        if pos_jogador in mapa.inimigos:
            inimigo = mapa.inimigos[pos_jogador]
            print(f"\n{inimigo.icone} Você encontrou um {inimigo.nome}!")
            resultado_batalha, pontos_batalha, experiencia = executar_batalha(
                jogador, inimigo, mapa, pos_jogador, posicao_anterior, stats
            )

            if resultado_batalha == "vitoria":
                pontos += pontos_batalha
                jogador.ganhar_experiencia(experiencia, stats)
                inimigos.remove(inimigo)
            elif resultado_batalha == "derrota":
                return pontos, False

        # --- Lógica de Eventos ---
        elif pos_jogador in eventos:
            evento = eventos[pos_jogador]
            print(f"\n{evento.icone} Você encontrou: {evento.nome}!")

            if evento == EnumEventos.FONTE_CURA:
                jogador.setVida(jogador.vida_maxima)
                pontos += 5
                stats["fontes_usadas"] += 1
                print("✨ Suas feridas foram curadas completamente! (+5 pontos)")
            
            elif evento == EnumEventos.CHARADA:
                acertou = resolver_charada()
                if acertou:
                    pontos += 20
                    stats["charadas_acertadas"] += 1
                    print("🎉 Resposta correta! Você ganhou sabedoria e pontos. (+20 pontos)")
                else:
                    stats["charadas_erradas"] += 1
                    print("❌ Resposta errada... O enigma desaparece.")
            
            elif evento == EnumEventos.BAU_TESOURO:
                pontos_bau = random.randint(15, 30)
                pontos += pontos_bau
                stats["baus_abertos"] += 1
                print(f"💰 Você abriu o baú e encontrou riquezas! (+{pontos_bau} pontos)")

            del eventos[pos_jogador]
            mapa.atualizar_posicao(*pos_jogador, jogador.icone)

        else:
            mapa.atualizar_posicao(*pos_jogador, jogador.icone)
        
    print(f"\n>>> {nome_fase} Concluída! <<<")
    return pontos + 20, True

def main():
    print("=== RPG PYTHON: EDIÇÃO BI ANALYTICS ===")
    nome = solicitar_nome()
    classe_escolhida = escolher_classe()

    # Inicializa Estatísticas
    stats = {
        "inicio_jogo": datetime.now(),
        "passos_dados": 0,
        "descansos": 0, # Novo KPI
        "inimigos_derrotados": 0,
        "fugas": 0,
        "mortes": 0,
        "baus_abertos": 0,
        "fontes_usadas": 0,
        "charadas_acertadas": 0,
        "charadas_erradas": 0,
        "experiencia_ganha": 0,
        "niveis_ganhos": 0,
        "criticos_acertados": 0,
        "criticos_sofridos": 0,
        "desvios": 0,
        "falhas_criticas_jogador": 0,
        "falhas_criticas_inimigos": 0,
    }

    fases = [
        {
            "nome": "Fase 1 - Floresta Nebulosa",
            "inimigos": {EnumInimigos.GOBLIN: 2, EnumInimigos.ZUMBI: 1},
            "qtd_eventos": 2
        },
        {
            "nome": "Fase 2 - Grutas Escuras",
            "inimigos": {EnumInimigos.ORC: 2, EnumInimigos.GOBLIN: 1},
            "qtd_eventos": 3
        },
        {
            "nome": "Fase 3 - Ruínas Antigas",
            "inimigos": {EnumInimigos.URSO: 1, EnumInimigos.ORC: 1, EnumInimigos.ZUMBI: 1},
            "qtd_eventos": 3
        },
    ]

    mapa = Mapa(LINHAS, COLUNAS)
    jogador = criar_jogador(nome, classe_escolhida, mapa)
    jogador.nome_classe_original_key = classe_escolhida.name 

    pontos = 0
    
    for fase in fases:
        mapa = Mapa(LINHAS, COLUNAS)
        jogador.mapa = mapa
        jogador.posicao = (0, 0)
        
        mapa.atualizar_posicao(*jogador.posicao, classe_escolhida.icone)

        inimigos_lista = gerar_inimigos_fase(fase["inimigos"], mapa)
        eventos_dict = gerar_eventos_fase(fase["qtd_eventos"], mapa)

        pontos, jogador_vivo = jogar_fase(
            jogador, mapa, inimigos_lista, eventos_dict, fase["nome"], pontos, stats
        )

        if not jogador_vivo:
            print("-" * 50)
            print(f"{nome.upper()} foi derrotado na {fase['nome']}.")
            print(f"Pontuação Final: {pontos}")
            print("-" * 50)
            registrar_pontuacao(nome, classe_escolhida, pontos, stats, jogador)
            return

    print("-" * 50)
    print(f"PARABÉNS, {nome.upper()}!")
    print(f"Pontuação Final: {pontos}")
    print("-" * 50)

    registrar_pontuacao(nome, classe_escolhida, pontos, stats, jogador)

if __name__ == "__main__":
    main()
