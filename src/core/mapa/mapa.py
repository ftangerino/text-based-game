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
# 🗺️  GERENCIAMENTO DO GRID DO JOGO
# -------------------------------------------------------------------------------------------------


class Mapa:
    """Classe utilitária para controlar posições, ícones e inimigos no grid."""
    def __init__(self, linhas, colunas, preenchimento="."):
        #  (.) representa um espaço vazio
        self.mapa = [[preenchimento for _ in range(colunas)] for _ in range(linhas)]
        self.linhas = linhas
        self.colunas = colunas
        self.inimigos = {}

    def exibir_mapa(self):
        for linha in self.mapa:
            print(" ".join(linha))

    def atualizar_posicao(self, x, y, simbolo):
        if 0 <= x < self.linhas and 0 <= y < self.colunas:
            self.mapa[x][y] = simbolo
        else:
            print("Posição fora do limite do mapa.")

    def obter_posicao(self, x, y):
        if 0 <= x < self.linhas and 0 <= y < self.colunas:
            return self.mapa[x][y]
        else:
            return None

    def esta_dentro_limites(self, x, y):
        return 0 <= x < self.linhas and 0 <= y < self.colunas

    def remover_posicao(self, x, y):
        self.atualizar_posicao(x, y, ".")

    def adicionar_inimigo(self, x, y, inimigo):
        if self.esta_dentro_limites(x, y):
            self.inimigos[(x, y)] = inimigo
            self.atualizar_posicao(x, y, "I")

    def remover_inimigo(self, x, y):
        if (x, y) in self.inimigos:
            del self.inimigos[(x, y)]
            self.remover_posicao(x, y)
