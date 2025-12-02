# /src/core/jogador.py

from ..entidade import Entidade
import time

class Jogador(Entidade):
    def __init__(self, nome, nivel, hp, mp, str, dex, int, def_, luk, mapa, posicao_inicial=(0, 0)):
        super().__init__(0, nome, nivel, hp, mp, str, dex, int, def_, luk)
        self.consumiveis = []
        self.items = []
        self.hp = hp
        self.vida_maxima = hp
        self.mapa = mapa
        self.posicao = posicao_inicial
        
        # Define um ícone padrão
        self.icone = "❤" 
        
        self.mapa.atualizar_posicao(*self.posicao, self.icone)  

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

    # ALTERAÇÃO AQUI: Adicionado parametro stats=None
    def mover_jogador_mapa(self, stats=None):
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
            -   Ir para Esquerda               - Checar Status
            -   Ir para Direita                - Descansar
            -   Ir para Cima                   
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
                        -   Ir para Esquerda               - Checar Status
                        -   Ir para Direita                - Descansar
                        -   Ir para Cima                   
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
                -   Ir para Esquerda               - Checar Status
                -   Ir para Direita                - Descansar
                -   Ir para Cima                   
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
                print(f"Você descansou e recuperou {cura} de vida")
            elif acao == mostrarStatus:
                print(self.toString())
            else: 
                print("""
____________________________________________________________________________________  
                            

                        Digite o comando corretamente

____________________________________________________________________________________
                """ )
            
    def toString(self):
        return (f"🛡️  {self.nome} (Lvl {self.nivel})\n"
                f"❤️  HP: {self.hp}/{self.vida_maxima} | 💧 MP: {self.mp}\n"
                f"💪 STR: {self.str} | 🎯 DEX: {self.dex} | 🧠 INT: {self.int}\n"
                f"🛡️ DEF: {self.def_} | 🍀 LUK: {self.luk}")