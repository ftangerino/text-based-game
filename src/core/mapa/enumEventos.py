from enum import Enum

class EnumEventos(Enum):
    FONTE_CURA = ("Fonte da Vida", "⛲")
    CHARADA = ("Esfinge Sábia", "📜")
    BAU_TESOURO = ("Baú de Tesouro", "💰")

    def __init__(self, nome, icone):
        self.nome = nome
        self.icone = icone