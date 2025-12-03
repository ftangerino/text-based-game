import psycopg2

def main():
    conn = psycopg2.connect(
        host="164.68.104.247",
        user="francisco",
        password="projetoFrancisco01",
        dbname="projpi"
    )

    try:
        cur = conn.cursor()

        # Garante que está no schema certo
        cur.execute("SET search_path TO jogo_pi;")

        print("=== Tabelas no schema jogo_pi ===")
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'jogo_pi'
            ORDER BY table_name;
        """)
        for (table_name,) in cur.fetchall():
            print("-", table_name)

        print("\n=== Views no schema jogo_pi ===")
        cur.execute("""
            SELECT table_name
            FROM information_schema.views
            WHERE table_schema = 'jogo_pi'
            ORDER BY table_name;
        """)
        for (view_name,) in cur.fetchall():
            print("-", view_name)

        # Ver estrutura de uma tabela, ex: sessao
        print("\n=== Colunas da tabela sessao ===")
        cur.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_schema = 'jogo_pi'
              AND table_name   = 'sessao'
            ORDER BY ordinal_position;
        """)
        for column_name, data_type, is_nullable in cur.fetchall():
            print(f"{column_name:30} {data_type:20} NULLABLE={is_nullable}")

        # Teste rápido de dados
        print("\n=== 5 primeiras linhas de sessao ===")
        cur.execute("SELECT * FROM sessao ORDER BY id LIMIT 5;")
        rows = cur.fetchall()
        for row in rows:
            print(row)

        # Teste da view de BI
        print("\n=== 5 primeiras linhas da view vw_fact_sessao ===")
        cur.execute("SELECT * FROM vw_fact_sessao ORDER BY sessao_id LIMIT 5;")
        rows = cur.fetchall()
        for row in rows:
            print(row)

    except Exception as e:
        print("Erro ao consultar o banco:", e)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
