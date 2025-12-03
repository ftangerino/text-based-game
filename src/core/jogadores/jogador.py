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
# 🧭 DEFINIÇÃO DE JOGADOR E HABILIDADES
# -------------------------------------------------------------------------------------------------
from ..entidade import Entidade
from .enumClasses import EnumClasses
from magias.enumMagia import enumMagia
from magias.enumTecnica import enumTecnica
from magias.enumTecnicasArqueiro import enumTecnicasArqueiro


class Jogador(Entidade):
    """Representa o personagem controlado pelo usuário e suas interações básicas."""
    def __init__(self, nome, nivel, hp, mp, str, dex, int, def_, luk, mapa, posicao_inicial=(0, 0)):
        super().__init__(0, nome, nivel, hp, mp, str, dex, int, def_, luk)
        self.consumiveis = []
        self.items = []
        self.vida_maxima = hp
        self.mapa = mapa
        self.posicao = posicao_inicial

        self.classe = None
        self.habilidades = []
        self._habilidades_para_desbloquear = []

        self.experiencia = 0
        self.proximo_nivel = self._calcular_experiencia_necessaria()

        # Define um ícone padrão
        self.icone = "❤"

        self.mapa.atualizar_posicao(*self.posicao, self.icone)

    ###################################################################################################
    # 🎯 PROGRESSÃO E HABILIDADES
    ###################################################################################################

    def definir_classe(self, classe: EnumClasses, stats=None):
        self.classe = classe

        # Ajusta ícone do mapa conforme a classe escolhida
        self.icone = classe.icone
        self.mapa.atualizar_posicao(*self.posicao, self.icone)

        if classe == EnumClasses.MAGO:
            fila = [magia.criar_magia() for magia in sorted(enumMagia, key=lambda m: m.nivel_requerido)]
        elif classe == EnumClasses.GUERREIRO:
            fila = [tec.criar_tecnica() for tec in sorted(enumTecnica, key=lambda t: t.nivel_requerido)]
        elif classe == EnumClasses.ARQUEIRO:
            fila = [tec.criar_tecnica() for tec in sorted(enumTecnicasArqueiro, key=lambda t: t.nivel_requerido)]
        else:
            fila = []

        self._habilidades_para_desbloquear = fila
        self.habilidades = []
        self._desbloquear_habilidades_por_nivel(stats)


    def _calcular_experiencia_necessaria(self):
        return 100 + (self.nivel - 1) * 50

    def _aplicar_bonus_nivel(self):
        incremento_hp = 10
        incremento_mp = 5
        incremento_atributos = 2

        self.nivel += 1
        self.vida_maxima += incremento_hp
        self.hp = self.vida_maxima
        self.mp += incremento_mp
        self.str += incremento_atributos
        self.dex += incremento_atributos
        self.int += incremento_atributos
        self.def_ += 1
        self.luk += 1

    def _desbloquear_habilidades_por_nivel(self, stats=None):
        desbloqueadas = []
        restantes = []

        for habilidade in self._habilidades_para_desbloquear:
            if self.nivel >= habilidade.nivel_requerido:
                self.habilidades.append(habilidade)
                desbloqueadas.append(habilidade.nome)
            else:
                restantes.append(habilidade)

        self._habilidades_para_desbloquear = restantes

        if stats is not None and desbloqueadas:
            stats["habilidades_desbloqueadas"] += len(desbloqueadas)
            print(f"✨ Novas habilidades: {', '.join(desbloqueadas)}")

    def ataque_basico(self):
        """Ataque padrão varia conforme a classe, devolvendo pelo menos 1 de dano base."""
        if self.classe == EnumClasses.MAGO:
            return max(1, self.str // 2)
        return max(1, self.str)

    def usar_habilidade(self, indice, stats=None):
        """Tenta executar uma habilidade pela posição na lista e atualiza métricas."""
        if not (0 <= indice < len(self.habilidades)):
            return None, "Habilidade inválida."

        habilidade = self.habilidades[indice]
        if habilidade.custo > self.mp:
            return None, "MP insuficiente para usar esta habilidade."

        self.mp -= habilidade.custo
        if stats is not None:
            stats["habilidades_usadas"] += 1
            if habilidade.tipo == "magia":
                stats["magias_lancadas"] += 1

        return habilidade, None

    def ganhar_experiencia(self, quantidade, stats=None):
        """Entrega experiência, níveis e desbloqueio automático conforme progressão."""
        if quantidade <= 0:
            return

        self.experiencia += quantidade
        if stats is not None:
            stats["experiencia_ganha"] += quantidade
        print(f"✨ Você ganhou {quantidade} de experiência. (Total: {self.experiencia}/{self.proximo_nivel})")

        while self.experiencia >= self.proximo_nivel:
            self.experiencia -= self.proximo_nivel
            self._aplicar_bonus_nivel()
            if stats is not None:
                stats["niveis_ganhos"] += 1
            self.proximo_nivel = self._calcular_experiencia_necessaria()
            self._desbloquear_habilidades_por_nivel(stats)
            print(
                f"⬆️  {self.nome} subiu para o nível {self.nivel}! "
                f"HP Máximo: {self.vida_maxima}, STR: {self.str}, DEX: {self.dex}, INT: {self.int}, "
                f"DEF: {self.def_}, LUK: {self.luk}"
            )
            print(f"Próximo nível em {self.proximo_nivel - self.experiencia} de XP.")

    def setVida(self, vida_atual):
        if vida_atual > self.vida_maxima:
            self.hp = self.vida_maxima
        else:
            self.hp = vida_atual

    def pegarConsumivel(self, consumivel):
        self.consumiveis.append(consumivel)

    def usarConsumivel(self, consumivel):
        self.hp += consumivel.hp
        self.mp += consumivel.mp

    def mostrarConsumivel(self):
        consumiveis_to_dict = {}
        for consumivel in self.consumiveis:
            if consumivel.nome in consumiveis_to_dict:
                consumiveis_to_dict[consumivel.nome] += 1
            else:
                consumiveis_to_dict[consumivel.nome] = 1

        todosItems = ["Items:\n"]
        for nome, quantidade in consumiveis_to_dict.items():
            todosItems.append(f"{nome}: {quantidade}")

        playerItems = "\n".join(todosItems)
        print(playerItems)

    ###################################################################################################
    # 🧭 MOVIMENTAÇÃO E INTERAÇÃO
    ###################################################################################################
    # ALTERAÇÃO AQUI: Adicionado parametro stats=None
    def mover_jogador_mapa(self, stats=None):
        """Recebe comando textual, move o jogador e contabiliza métricas de descanso."""
        movimentos = {
            "esquerda": (0, -1),
            "direita": (0, 1),
            "cima": (-1, 0),
            "baixo": (1, 0)
        }
        descansar = "descansar"
        mostrar_status = "checar status"
        print("""
____________________________________________________________________________________  
                            
                O que você deseja fazer?
                Ações de Movimento:                 Ações de Descanso:
                -   Esquerda | Direita               - Checar Status
                -   Cima     | Baixo                 - Descansar
____________________________________________________________________________________
                """ )
        while True:
            acao = input("Digite a ação que deseja realizar: ").lower()
            if acao in movimentos:
                dx, dy = movimentos[acao]
                novo_x = self.posicao[0] + dx
                novo_y = self.posicao[1] + dy
                if self.mapa.esta_dentro_limites(novo_x, novo_y):
                    self.mapa.remover_posicao(*self.posicao)
                    self.posicao = (novo_x, novo_y)
                    self.mapa.atualizar_posicao(*self.posicao, self.icone)
                    print(f"Você se moveu para {acao}.")
                    print("""
        ____________________________________________________________________________________

                O que você deseja fazer?
                Ações de Movimento:                 Ações de Descanso:
                -   Esquerda | Direita               - Checar Status
                -   Cima     | Baixo                 - Descansar
        ____________________________________________________________________________________
                        """ )
                    self.mapa.exibir_mapa()
                    break
                else:
                    print("Movimento inválido! Fora dos limites do mapa.")

            elif acao == descansar:
                cura = int(self.vida_maxima * 0.1) # Converti para int para ficar bonito
                self.setVida(self.hp + cura)

                # ALTERAÇÃO AQUI: Contabiliza o descanso se stats foi passado
                if stats is not None:
                    stats["descansos"] += 1

                print(f"Você descansou e recuperou {cura} de vida.")

            elif acao == mostrar_status:
                print(self.toString())

            else:
                print("Comando inválido. Tente novamente.")


    def mover(self):
        # legacy -v
        esquerda = "esquerda"
        direita = "direita"
        cima = "cima"
        descansar = "descansar"
        mostrarStatus = "checar status"
        count = 0
        while True:
            count += 1
            if count == 100:
                break
            print("""
____________________________________________________________________________________

                O que você deseja fazer?
                Ações de Movimento:                 Ações de Descanso:
                -   Esquerda | Direita               - Checar Status
                -   Cima     | Baixo                 - Descansar
____________________________________________________________________________________
                """ )
            print("Digite a ação que deseja realizar:", end=" ")
            acao = input().lower()
            if acao in [esquerda, direita, cima]:
                print(f"Você foi para {acao}")
                break
            elif acao == descansar:
                cura = self.hp * 0.1
                self.setVida(self.hp + cura)
                self.setMp(self.mp + cura)
                print(f"Você descansou e recuperou {cura} de vida e mana")
            elif acao == mostrarStatus:
                print(self.toString())
            else:
                print("""
____________________________________________________________________________________


                        Digite o comando corretamente

____________________________________________________________________________________
                """ )

    def toString(self):
        return (
            f"🛡️  {self.nome} (Lvl {self.nivel})\n"
            f"❤️  HP: {self.hp}/{self.vida_maxima} | 💧 MP: {self.mp}\n"
            f"✨ XP: {self.experiencia}/{self.proximo_nivel}\n"
            f"💪 STR: {self.str} | 🎯 DEX: {self.dex} | 🧠 INT: {self.int}\n"
            f"🛡️ DEF: {self.def_} | 🍀 LUK: {self.luk}"
        )
