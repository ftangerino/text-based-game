class Magia:
    def __init__(self, nome, dano, custo, nivel_requerido=1, atributo_base="int", tipo="magia"):
        self.nome = nome
        self.dano = dano
        self.custo = custo
        self.nivel_requerido = nivel_requerido
        self.atributo_base = atributo_base
        self.tipo = tipo

    def calcular_dano(self, jogador):
        atributo = getattr(jogador, self.atributo_base, 0)
        bonus = atributo // (2 if self.tipo == "magia" else 3)
        return max(1, self.dano + bonus)
