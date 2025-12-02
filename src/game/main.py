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
        print(f"{idx}. {classe.nome} {classe.icone}") # Mostra o ícone na seleção

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
            # Verifica se está vazio e não é a posição inicial
            if (x, y) != (0, 0) and mapa.obter_posicao(x, y) == ".":
                # Tenta usar o ícone do Enum, se o Mapa suportar, ou passa o objeto
                # Assumindo que o seu mapa.adicionar_inimigo lida com o objeto ou string
                # Aqui passamos o ícone para visualização no mapa
                mapa.adicionar_inimigo(x, y, inimigo) 
                
                # Se o seu método mapa.adicionar_inimigo desenhar baseado no nome, 
                # talvez precise alterar o mapa.py. 
                # Se ele desenhar apenas um caractere fixo, usamos este truque:
                # mapa.matriz[x][y] = inimigo.icone (se tiver acesso direto à matriz)
                break
    return inimigos

def gerar_eventos_fase(quantidade: int, mapa: Mapa) -> Dict[Tuple[int, int], EnumEventos]:
    """Gera eventos aleatórios no mapa (Fonte, Charada, Baú)."""
    eventos_ativos = {}
    tipos_eventos = [EnumEventos.FONTE_CURA, EnumEventos.CHARADA, EnumEventos.BAU_TESOURO]
    
    for _ in range(quantidade):
        evento_escolhido = random.choice(tipos_eventos)
        while True:
            x, y = random.randint(0, LINHAS - 1), random.randint(0, COLUNAS - 1)
            # Não coloca evento no 0,0, nem onde tem inimigo, nem onde já tem evento
            if (x, y) != (0, 0) and mapa.obter_posicao(x, y) == "." and (x,y) not in eventos_ativos:
                # Adiciona visualmente ao mapa
                mapa.atualizar_posicao(x, y, evento_escolhido.icone)
                eventos_ativos[(x, y)] = evento_escolhido
                break
    return eventos_ativos

def resolver_charada() -> bool:
    """Banco de charadas simples."""
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

def jogar_fase(jogador: Jogador, mapa: Mapa, inimigos: List[EnumInimigos], eventos: Dict, nome_fase: str, pontos: int) -> int:
    print(f"\n=== Iniciando {nome_fase}! ===")
    mapa.exibir_mapa()

    while inimigos:
        # Move o jogador
        jogador.mover_jogador_mapa()
        pos_jogador = jogador.posicao
        
        # --- Lógica de Inimigos ---
        if pos_jogador in mapa.inimigos:
            inimigo = mapa.inimigos[pos_jogador]
            print(f"\n{inimigo.icone} Você encontrou um {inimigo.nome}!")
            
            op = input("[1] Atacar | [Sair] Fugir: ").lower()
            if op == "sair":
                print("Você fugiu! Fim de jogo.")
                sys.exit()
            elif op == "1":
                mapa.remover_inimigo(*pos_jogador)
                if inimigo in inimigos:
                    inimigos.remove(inimigo)
                pontos += 10
                print(f"Vitória! Inimigo derrotado. (+10 pontos)")
            
            # Reinsere o ícone do jogador na posição atual após matar inimigo
            mapa.atualizar_posicao(*pos_jogador, jogador.icone)

        # --- Lógica de Eventos ---
        elif pos_jogador in eventos:
            evento = eventos[pos_jogador]
            print(f"\n{evento.icone} Você encontrou: {evento.nome}!")

            if evento == EnumEventos.FONTE_CURA:
                jogador.setVida(jogador.vida_maxima)
                pontos += 5
                print("✨ Suas feridas foram curadas completamente! (+5 pontos)")
            
            elif evento == EnumEventos.CHARADA:
                acertou = resolver_charada()
                if acertou:
                    pontos += 20
                    print("🎉 Resposta correta! Você ganhou sabedoria e pontos. (+20 pontos)")
                else:
                    print("❌ Resposta errada... O enigma desaparece.")
            
            elif evento == EnumEventos.BAU_TESOURO:
                pontos_bau = random.randint(15, 30)
                pontos += pontos_bau
                print(f"💰 Você abriu o baú e encontrou riquezas! (+{pontos_bau} pontos)")

            # Remove o evento do mapa após interagir
            del eventos[pos_jogador]
            # Atualiza visualmente para mostrar o jogador em cima do local do evento
            mapa.atualizar_posicao(*pos_jogador, jogador.icone)

        else:
            # Se não tem nada, garante que o ícone do jogador está lá
            mapa.atualizar_posicao(*pos_jogador, jogador.icone)
        
        # mapa.exibir_mapa() # Opcional: mostrar mapa a cada passo

    print(f"\n>>> {nome_fase} Concluída! <<<")
    return pontos + 20

def main():
    print("=== RPG PYTHON: EDIÇÃO ÉPICA ===")
    nome = solicitar_nome()
    classe_escolhida = escolher_classe()

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
    pontos = 0
    
    for fase in fases:
        # Resetar Mapa e Posição
        mapa = Mapa(LINHAS, COLUNAS)
        jogador.mapa = mapa
        jogador.posicao = (0, 0)
        
        # Coloca o ícone do jogador no início (usando o ícone da classe)
        mapa.atualizar_posicao(*jogador.posicao, classe_escolhida.icone) 

        inimigos_lista = gerar_inimigos_fase(fase["inimigos"], mapa)
        
        # Gera eventos (Fontes, Charadas, Baús)
        eventos_dict = gerar_eventos_fase(fase["qtd_eventos"], mapa)

        pontos = jogar_fase(jogador, mapa, inimigos_lista, eventos_dict, fase["nome"], pontos)

    print("-" * 50)
    print(f"PARABÉNS, {nome.upper()}!")
    print(f"Pontuação Final: {pontos}")
    print("-" * 50)
    registrar_pontuacao(nome, classe_escolhida, pontos)

if __name__ == "__main__":
    main()