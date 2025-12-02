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

def registrar_pontuacao(nome: str, classe: EnumClasses, pontos: int, stats: Dict) -> None:
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
            "combate": {
                "inimigos_derrotados": stats["inimigos_derrotados"],
                "fugas": stats["fugas"]
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

def jogar_fase(jogador: Jogador, mapa: Mapa, inimigos: List[EnumInimigos], eventos: Dict, nome_fase: str, pontos: int, stats: Dict) -> int:
    print(f"\n=== Iniciando {nome_fase}! ===")
    mapa.exibir_mapa()

    while inimigos:
        # Passa stats para contabilizar descansos
        jogador.mover_jogador_mapa(stats) 
        
        stats["passos_dados"] += 1 
        
        pos_jogador = jogador.posicao
        
        # --- Lógica de Inimigos ---
        if pos_jogador in mapa.inimigos:
            inimigo = mapa.inimigos[pos_jogador]
            print(f"\n{inimigo.icone} Você encontrou um {inimigo.nome}!")
            
            # Loop de batalha simples
            while True:
                op = input("[1] Atacar | [Sair] Fugir: ").lower()
                
                if op == "sair":
                    print("🏃 Você fugiu! O inimigo perdeu interesse e sumiu.")
                    stats["fugas"] += 1
                    
                    # Remove o inimigo do mapa e da lista lógica
                    mapa.remover_inimigo(*pos_jogador)
                    if inimigo in inimigos:
                        inimigos.remove(inimigo)
                    
                    # Atualiza visualmente para o jogador voltar para a posição
                    mapa.atualizar_posicao(*pos_jogador, jogador.icone)
                    
                    # Sai do loop de batalha (break), mas continua na fase (while inimigos)
                    break 

                elif op == "1":
                    mapa.remover_inimigo(*pos_jogador)
                    if inimigo in inimigos:
                        inimigos.remove(inimigo)
                    pontos += 10
                    stats["inimigos_derrotados"] += 1
                    print(f"Vitória! Inimigo derrotado. (+10 pontos)")
                    mapa.atualizar_posicao(*pos_jogador, jogador.icone)
                    break # Sai do loop de batalha
                else:
                    print("Opção inválida.")

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
    return pontos + 20

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
        "baus_abertos": 0,
        "fontes_usadas": 0,
        "charadas_acertadas": 0,
        "charadas_erradas": 0
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

        pontos = jogar_fase(jogador, mapa, inimigos_lista, eventos_dict, fase["nome"], pontos, stats)

    print("-" * 50)
    print(f"PARABÉNS, {nome.upper()}!")
    print(f"Pontuação Final: {pontos}")
    print("-" * 50)
    
    registrar_pontuacao(nome, classe_escolhida, pontos, stats)

if __name__ == "__main__":
    main()