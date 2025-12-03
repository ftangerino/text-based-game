###################################################################################################
# 📥 IMPORTS | CODING: UTF-8
###################################################################################################
# ✅ → Discussed and realized
# 🟢 → Discussed and not realized (to be done after the meeting)
# 🟡 → Little important and not discussed (unhindered)
# 🔴 → Very important and not discussed (hindered)
# ❌ → Canceled
# ⚪ → Postponed (technical debit)
###################################################################################################
# -------------------------------------------------------------------------------------------------
# 🔰 PILHA DE IMPORTS (BASE DO LOOP DE JOGO)
# -------------------------------------------------------------------------------------------------
import sys
import json
import os
import random
from datetime import datetime
from typing import Dict, List, Tuple

import psycopg2

# Adiciona o diretório pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.jogadores.jogador import Jogador
from core.inimigos.enumInimigos import EnumInimigos
from core.jogadores.enumClasses import EnumClasses
from core.mapa.mapa import Mapa
from core.mapa.enumEventos import EnumEventos

###################################################################################################
# 📃 PARÂMETROS GLOBAIS
###################################################################################################
# ✅ Tamanho padrão do tabuleiro e opções de conexão.
LINHAS = 5
COLUNAS = 5

# 🔴 Ajuste as credenciais conforme o ambiente ou via variáveis de ambiente.
DB_CONFIG = {
    "host": "164.68.104.247",
    "user": "francisco",
    "password": "projetoFrancisco01",
    "dbname": "projpi",
}


###################################################################################################
# 🧭 FLUXO DE ENTRADA DO JOGADOR
###################################################################################################
def solicitar_nome() -> str:
    """Solicita um nome não vazio para o personagem principal."""
    while True:
        nome = input("Digite o nome do seu personagem: ").strip()
        if nome:
            return nome
        print("O nome não pode ser vazio.")


def escolher_classe() -> EnumClasses:
    """Apresenta as classes disponíveis e retorna a escolha do usuário."""
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
    """Instancia um jogador com ícone e vida máxima inicial alinhados à classe."""
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


###################################################################################################
# 🎲 GERAÇÃO PROCEDURAL DE FASES
###################################################################################################
def gerar_inimigos_fase(
    configuracao: Dict[EnumInimigos, int],
    mapa: Mapa,
    chefe_final: EnumInimigos | None = None,
    posicao_chefe: Tuple[int, int] | None = None,
) -> List[EnumInimigos]:
    """Sorteia posições no mapa e posiciona inimigos comuns e chefe da fase."""
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

    if chefe_final:
        alvo_x, alvo_y = posicao_chefe if posicao_chefe else (LINHAS - 1, COLUNAS - 1)
        while not mapa.esta_dentro_limites(alvo_x, alvo_y) or mapa.obter_posicao(alvo_x, alvo_y) != ".":
            alvo_x, alvo_y = random.randint(0, LINHAS - 1), random.randint(0, COLUNAS - 1)

        mapa.adicionar_inimigo(alvo_x, alvo_y, chefe_final)
        inimigos.append(chefe_final)

    return inimigos


def gerar_eventos_fase(quantidade: int, mapa: Mapa) -> Dict[Tuple[int, int], EnumEventos]:
    """Distribui eventos aleatórios garantindo que não se sobreponham no grid."""
    eventos_ativos = {}
    tipos_eventos = [EnumEventos.FONTE_CURA, EnumEventos.CHARADA, EnumEventos.BAU_TESOURO]

    for _ in range(quantidade):
        evento_escolhido = random.choice(tipos_eventos)
        while True:
            x, y = random.randint(0, LINHAS - 1), random.randint(0, COLUNAS - 1)
            if (x, y) != (0, 0) and mapa.obter_posicao(x, y) == "." and (x, y) not in eventos_ativos:
                mapa.atualizar_posicao(x, y, evento_escolhido.icone)
                eventos_ativos[(x, y)] = evento_escolhido
                break
    return eventos_ativos


def resolver_charada() -> bool:
    """Apresenta uma charada aleatória e retorna True se o jogador acertar."""
    charadas = [
        ("O que é, o que é? Cai em pé e corre deitado?", "chuva"),
        ("O que é, o que é? Tem cabeça e tem dente, não é bicho e nem é gente?", "alho"),
        ("Quanto mais se tira, maior fica?", "buraco"),
        ("O que sempre está na sua frente, mas você não consegue ver?", "futuro"),
    ]
    pergunta, resposta_certa = random.choice(charadas)
    print(f"\n📜 CHARADA: {pergunta}")
    resposta = input("Sua resposta: ").lower().strip()
    return resposta == resposta_certa


###################################################################################################
# 📊 PERSISTÊNCIA E MÉTRICAS
###################################################################################################
def registrar_pontuacao(
    nome: str, classe: EnumClasses, pontos: int, stats: Dict, jogador: Jogador
) -> None:
    """Salva um snapshot local em JSON para manter um histórico offline."""
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
            "descansos_realizados": stats["descansos"],
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
                "habilidades_usadas": stats["habilidades_usadas"],
                "magias_lancadas": stats["magias_lancadas"],
                "habilidades_desbloqueadas": stats["habilidades_desbloqueadas"],
            },
            "eventos": {
                "baus_abertos": stats["baus_abertos"],
                "fontes_usadas": stats["fontes_usadas"],
                "charadas_acertadas": stats["charadas_acertadas"],
                "charadas_erradas": stats["charadas_erradas"],
            },
        },
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


# ============================
# SALVAR PROGRESSO NO POSTGRES
# ============================

def salvar_progresso_db(
    nome: str, classe: EnumClasses, pontos: int, stats: Dict, jogador: Jogador
) -> None:
    """
    Salva/atualiza o progresso da sessão atual no Postgres.
    - Na primeira chamada: cria jogador, classe e sessão (sessao_id fica em stats).
    - Nas próximas: atualiza a mesma sessão até o jogador ganhar ou morrer.
    """
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # Garante o schema correto
        cur.execute("SET search_path TO jogo_pi;")

        # Upsert de classe
        cur.execute(
            """
            INSERT INTO classe (nome)
            VALUES (%s)
            ON CONFLICT (nome)
            DO UPDATE SET nome = EXCLUDED.nome
            RETURNING id;
            """,
            (classe.nome,),
        )
        classe_id = cur.fetchone()[0]

        # Upsert de jogador
        cur.execute(
            """
            INSERT INTO jogador (nome)
            VALUES (%s)
            ON CONFLICT (nome)
            DO UPDATE SET nome = EXCLUDED.nome
            RETURNING id;
            """,
            (nome,),
        )
        jogador_id = cur.fetchone()[0]

        # Cria a sessão na primeira vez
        if stats.get("sessao_id") is None:
            cur.execute(
                """
                INSERT INTO sessao (jogador_id, classe_id, horario, pontos)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
                """,
                (jogador_id, classe_id, stats["inicio_jogo"], pontos),
            )
            sessao_id = cur.fetchone()[0]
            stats["sessao_id"] = sessao_id
        else:
            sessao_id = stats["sessao_id"]
            cur.execute(
                """
                UPDATE sessao
                SET pontos = %s
                WHERE id = %s;
                """,
                (pontos, sessao_id),
            )

        # Tempo de sessão até o momento
        tempo_total = int((datetime.now() - stats["inicio_jogo"]).total_seconds())

        # Métricas gerais
        cur.execute(
            """
            INSERT INTO sessao_metricas (
                sessao_id,
                tempo_sessao_segundos,
                passos_totais,
                descansos_realizados,
                nivel_final,
                experiencia_total_ganha,
                niveis_ganhos
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (sessao_id) DO UPDATE SET
                tempo_sessao_segundos   = EXCLUDED.tempo_sessao_segundos,
                passos_totais           = EXCLUDED.passos_totais,
                descansos_realizados    = EXCLUDED.descansos_realizados,
                nivel_final             = EXCLUDED.nivel_final,
                experiencia_total_ganha = EXCLUDED.experiencia_total_ganha,
                niveis_ganhos           = EXCLUDED.niveis_ganhos;
            """,
            (
                sessao_id,
                tempo_total,
                stats["passos_dados"],
                stats["descansos"],
                jogador.nivel,
                stats["experiencia_ganha"],
                stats["niveis_ganhos"],
            ),
        )

        # Métricas de combate
        cur.execute(
            """
            INSERT INTO sessao_metricas_combate (
                sessao_id,
                inimigos_derrotados,
                fugas,
                criticos_acertados,
                criticos_sofridos,
                desvios,
                falhas_criticas_jogador,
                falhas_criticas_inimigos,
                habilidades_usadas,
                magias_lancadas,
                habilidades_desbloqueadas
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (sessao_id) DO UPDATE SET
                inimigos_derrotados       = EXCLUDED.inimigos_derrotados,
                fugas                     = EXCLUDED.fugas,
                criticos_acertados        = EXCLUDED.criticos_acertados,
                criticos_sofridos         = EXCLUDED.criticos_sofridos,
                desvios                   = EXCLUDED.desvios,
                falhas_criticas_jogador   = EXCLUDED.falhas_criticas_jogador,
                falhas_criticas_inimigos  = EXCLUDED.falhas_criticas_inimigos,
                habilidades_usadas        = EXCLUDED.habilidades_usadas,
                magias_lancadas           = EXCLUDED.magias_lancadas,
                habilidades_desbloqueadas = EXCLUDED.habilidades_desbloqueadas;
            """,
            (
                sessao_id,
                stats["inimigos_derrotados"],
                stats["fugas"],
                stats["criticos_acertados"],
                stats["criticos_sofridos"],
                stats["desvios"],
                stats["falhas_criticas_jogador"],
                stats["falhas_criticas_inimigos"],
                stats["habilidades_usadas"],
                stats["magias_lancadas"],
                stats["habilidades_desbloqueadas"],
            ),
        )

        # Métricas de eventos
        cur.execute(
            """
            INSERT INTO sessao_metricas_eventos (
                sessao_id,
                baus_abertos,
                fontes_usadas,
                charadas_acertadas,
                charadas_erradas
            )
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (sessao_id) DO UPDATE SET
                baus_abertos       = EXCLUDED.baus_abertos,
                fontes_usadas      = EXCLUDED.fontes_usadas,
                charadas_acertadas = EXCLUDED.charadas_acertadas,
                charadas_erradas   = EXCLUDED.charadas_erradas;
            """,
            (
                sessao_id,
                stats["baus_abertos"],
                stats["fontes_usadas"],
                stats["charadas_acertadas"],
                stats["charadas_erradas"],
            ),
        )

        conn.commit()
        print(f"[BI][DB] Progresso salvo/atualizado (sessao_id={sessao_id}).")

    except Exception as e:
        print(f"[BI][ERRO] Falha ao salvar progresso no banco: {e}")
    finally:
        if conn:
            conn.close()


###################################################################################################
# ⚔️ MECÂNICAS DE COMBATE
###################################################################################################
def calcular_chance_acerto(atacante_dex: int, defesa_defensor: int, evasao_defensor: int) -> float:
    """Calcula chance de acerto ponderando destreza do atacante e defesa do alvo."""
    defesa = (defesa_defensor + evasao_defensor) / 2
    chance = 0.7 + (atacante_dex - defesa) * 0.01
    return max(0.1, min(0.95, chance))


def eh_critico(luk_atacante: int) -> bool:
    """Determina se o ataque será crítico com base na sorte do atacante."""
    chance_critico = min(0.5, 0.05 + luk_atacante / 100)
    return random.random() < chance_critico


def calcular_dano(str_atacante: int, def_defensor: int, critico: bool) -> int:
    """Gera dano final a partir da força, defesa e flag de crítico."""
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
    """Resolve uma batalha por turnos e devolve status, pontos e XP ganhos."""
    inimigo_hp = inimigo.hp

    while True:
        print(
            f"\n❤️ {jogador.nome}: {jogador.hp}/{jogador.vida_maxima} | "
            f"{inimigo.icone} {inimigo.nome}: {inimigo_hp}/{inimigo.hp}"
        )
        op = input("[1] Ataque básico | [2] Habilidade | [Sair] Fugir: ").lower()

        if op == "sair":
            print("🏃 Você fugiu! O inimigo permanece no mapa.")
            stats["fugas"] += 1
            mapa.atualizar_posicao(*posicao_inimigo, "I")
            mapa.atualizar_posicao(*posicao_anterior, jogador.icone)
            jogador.posicao = posicao_anterior
            mapa.exibir_mapa()
            return "fugiu", 0, 0

        habilidade_usada = None
        if op == "2":
            if not jogador.habilidades:
                print("Você ainda não possui habilidades desbloqueadas. Usando ataque básico.")
            else:
                print("\nEscolha uma habilidade:")
                for idx, habilidade in enumerate(jogador.habilidades, start=1):
                    print(
                        f"[{idx}] {habilidade.nome} | Dano base: {habilidade.dano} | "
                        f"Custo: {habilidade.custo} MP"
                    )
                escolha_habilidade = input("Opção: ")
                if not escolha_habilidade.isdigit():
                    print("Entrada inválida. Tente novamente.")
                    continue
                habilidade_indice = int(escolha_habilidade) - 1
                habilidade_usada, erro = jogador.usar_habilidade(habilidade_indice, stats)
                if erro:
                    print(erro)
                    continue

        elif op != "1":
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
            if habilidade_usada:
                dano_base = habilidade_usada.calcular_dano(jogador)
                defesa_ajustada = inimigo.def_ // (3 if habilidade_usada.tipo == "magia" else 2)
                dano = max(1, dano_base - defesa_ajustada)
                acao_texto = f"usou {habilidade_usada.nome}"
            else:
                dano = calcular_dano(jogador.ataque_basico(), inimigo.def_, False)
                acao_texto = "atacou"

            if critico:
                dano *= 2
                stats["criticos_acertados"] += 1
            mensagem_critico = " (CRÍTICO!)" if critico else ""

            inimigo_hp = max(0, inimigo_hp - dano)
            print(
                f"🗡️ Você {acao_texto} e causou {dano} de dano"
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
    """Executa movimentação, combate e eventos até concluir a fase ou o jogador cair."""
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


###################################################################################################
# 🧭 LOOP PRINCIPAL E CAMPANHAS
###################################################################################################
def main():
    print("=== RPG PYTHON: EDIÇÃO BI ANALYTICS ===")
    nome = solicitar_nome()
    classe_escolhida = escolher_classe()

    # Inicializa Estatísticas
    stats = {
        "inicio_jogo": datetime.now(),
        "passos_dados": 0,
        "descansos": 0,
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
        "habilidades_usadas": 0,
        "magias_lancadas": 0,
        "habilidades_desbloqueadas": 0,
        "sessao_id": None,
    }

    setups_de_fases = [
        {
            "nome": "Trilha do Reino",
            "descricao": "Uma jornada clássica por planícies abertas, uma floresta viva e um castelo profano.",
            "fases": [
                {
                    "nome": "Planície Dourada",
                    "descricao": "Campos ensolarados onde bandidos e lobos espreitam viajantes.",
                    "inimigos": {
                        EnumInimigos.BANDIDO: 2,
                        EnumInimigos.LOBO: 2,
                        EnumInimigos.URUBU: 1,
                    },
                    "qtd_eventos": 2,
                },
                {
                    "nome": "Floresta Ancestral",
                    "descricao": "Bosque fechado guardado por goblins, aranhas e espíritos antigos.",
                    "inimigos": {
                        EnumInimigos.GOBLIN: 2,
                        EnumInimigos.ARANHA: 2,
                        EnumInimigos.TREANT: 1,
                        EnumInimigos.ESPIRITO_FLORESTA: 1,
                    },
                    "qtd_eventos": 3,
                },
                {
                    "nome": "Castelo Profano",
                    "descricao": "Salões tomados por bruxas e cavaleiros corrompidos culminando em um Lich.",
                    "inimigos": {
                        EnumInimigos.ESQUELETO: 2,
                        EnumInimigos.BRUXA: 1,
                        EnumInimigos.CAVALEIRO_NEGRO: 1,
                        EnumInimigos.FEITICEIRO_SOMBRIO: 1,
                    },
                    "qtd_eventos": 3,
                    "chefe": EnumInimigos.LICH,
                },
            ],
        },
        {
            "nome": "Rota das Cinzas",
            "descricao": "Uma marcha por planícies arrasadas, floresta mística e um castelo demoníaco.",
            "fases": [
                {
                    "nome": "Planície Ventosa",
                    "descricao": "Terreno aberto com bandidos endurecidos e carcaças vigiadas por urubus.",
                    "inimigos": {
                        EnumInimigos.BANDIDO: 2,
                        EnumInimigos.LOBO: 1,
                        EnumInimigos.URSO: 1,
                        EnumInimigos.URUBU: 1,
                    },
                    "qtd_eventos": 2,
                },
                {
                    "nome": "Floresta Crepuscular",
                    "descricao": "Mata cheia de espíritos, lobisomens e druidas torcidos pela magia.",
                    "inimigos": {
                        EnumInimigos.LOBISOMEM: 1,
                        EnumInimigos.ESPIRITO_FLORESTA: 2,
                        EnumInimigos.TREANT: 1,
                        EnumInimigos.FEITICEIRO_SOMBRIO: 1,
                    },
                    "qtd_eventos": 3,
                },
                {
                    "nome": "Castelo Infernal",
                    "descricao": "Fortaleza ardente repleta de armaduras animadas e magia sombria até o grande demônio.",
                    "inimigos": {
                        EnumInimigos.ARMADURA_VIVA: 2,
                        EnumInimigos.CAVALEIRO_NEGRO: 1,
                        EnumInimigos.FEITICEIRO_SOMBRIO: 1,
                    },
                    "qtd_eventos": 3,
                    "chefe": EnumInimigos.DEMONIO,
                },
            ],
        },
    ]

    setup_escolhido = random.choice(setups_de_fases)
    print(f"\n🌍 Caminho escolhido: {setup_escolhido['nome']}")
    print(setup_escolhido["descricao"])

    fases = setup_escolhido["fases"]

    mapa = Mapa(LINHAS, COLUNAS)
    jogador = criar_jogador(nome, classe_escolhida, mapa)
    jogador.definir_classe(classe_escolhida, stats)
    jogador.nome_classe_original_key = classe_escolhida.name

    pontos = 0

    for fase in fases:
        mapa = Mapa(LINHAS, COLUNAS)
        jogador.mapa = mapa
        jogador.posicao = (0, 0)

        mapa.atualizar_posicao(*jogador.posicao, classe_escolhida.icone)

        inimigos_lista = gerar_inimigos_fase(
            fase["inimigos"],
            mapa,
            chefe_final=fase.get("chefe"),
        )
        eventos_dict = gerar_eventos_fase(fase["qtd_eventos"], mapa)

        if "descricao" in fase:
            print(f"{fase['descricao']}")

        pontos, jogador_vivo = jogar_fase(
            jogador, mapa, inimigos_lista, eventos_dict, fase["nome"], pontos, stats
        )
        salvar_progresso_db(nome, classe_escolhida, pontos, stats, jogador)

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
    salvar_progresso_db(nome, classe_escolhida, pontos, stats, jogador)


if __name__ == "__main__":
    main()
