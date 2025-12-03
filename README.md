# RPG Tático em Texto

Uma aventura interativa em Python que combina exploração em grade, combate em turnos e coleta de métricas para BI. O jogo permite escolher classes, enfrentar inimigos variados, interagir com eventos do mapa e registrar o progresso tanto em arquivo local (`scores.json`) quanto em um banco PostgreSQL.

## 🚀 Principais recursos
- **Exploração em mapa 5x5** com posicionamento aleatório de inimigos e eventos.
- **Combate em turnos** com ataques básicos, habilidades desbloqueáveis e chances de crítico/erro.
- **Classes jogáveis** (guerreiro, mago etc.) com atributos e ícones próprios.
- **Eventos de mapa** (fontes de cura, charadas, baús de tesouro) que concedem pontos e bônus.
- **Coleta de métricas** de sessão (passos, descanso, combates, magias usadas) e persistência opcional em PostgreSQL.

## 🧰 Pré-requisitos
- Python 3.12+ (testado localmente)
- Dependências Python: `psycopg2-binary` para integração com PostgreSQL e `python-dotenv` caso queira carregar variáveis de ambiente.
- Banco PostgreSQL opcional, com schema `jogo_pi` disponível e credenciais ajustadas em `src/game/main.py`.

Instale as dependências com:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install psycopg2-binary python-dotenv
```

## ▶️ Como jogar
1. No diretório raiz, ative o ambiente virtual e execute:
   ```bash
   python -m src.game.main
   ```
2. Informe o nome do personagem e escolha uma classe.
3. Navegue pelo mapa com os comandos apresentados em tela, interagindo com eventos e enfrentando inimigos.
4. Ao concluir ou ser derrotado, o jogo registra métricas em `data/scores.json` e, se o banco estiver acessível, atualiza o progresso no PostgreSQL.

## 🗄️ Persistência e BI
- **JSON local**: todos os registros ficam em `src/data/scores.json` para histórico rápido.
- **PostgreSQL**: ajuste o dicionário `DB_CONFIG` em `src/game/main.py` ou utilize variáveis de ambiente carregadas via `python-dotenv`. A função `salvar_progresso_db` realiza upsert de jogadores, classes e métricas por sessão.

## 🧭 Estrutura do projeto
```
text-based-game/
├─ README.md                  # Este guia
├─ docs/README.md             # Alias para a documentação
├─ src/
│  ├─ game/main.py            # Loop do jogo, geração de fases e salvamento de métricas
│  ├─ core/                   # Mecânicas centrais (mapa, combate, entidades)
│  ├─ magias/                 # Magias e técnicas das classes
│  └─ data/                   # Base local de pontuações
```

## 🧪 Testes
Os arquivos em `src/tests/` são esboços interativos e dependem de entrada do usuário. Não há suíte automatizada configurada; execute-os apenas para validação manual.

## 💡 Dicas rápidas
- Mantenha o mapa visível para não esquecer onde estão inimigos (`I`) e eventos especiais.
- Use descansos com moderação para recuperar HP, mas fique atento aos pontos e ao ritmo das fases.
- Explore diferentes classes para destravar habilidades exclusivas e aumentar as métricas de magia ou técnica.
