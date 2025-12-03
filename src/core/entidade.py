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
# 🧱 MODELO BÁSICO DE ENTIDADE
# -------------------------------------------------------------------------------------------------


class Entidade:
    """Base de atributos compartilhados entre jogadores e inimigos."""
    def __init__(self, id, nome, nivel, hp, mp, str, dex, int, def_, luk):
        self.id = id
        self.nome = nome
        self.nivel = nivel
        self.hp = hp
        self.mp = mp
        self.str = str
        self.dex = dex
        self.int = int
        self.def_ = def_
        self.luk = luk

    def toString(self):
        return (
            f"Nome: {self.nome} Nivel: {self.nivel}\n"
            f"HP: {self.hp}\nMP: {self.mp}\nSTR: {self.str}\nDEX: {self.dex}\n"
            f"INT: {self.int}\nDEF: {self.def_}\nLUK: {self.luk}"
        )
