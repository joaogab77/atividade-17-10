import sqlite3

def conectar_banco(caminho_banco):
    try:

        conexao = sqlite3.connect(caminho_banco)
        print(f"Conexão com {caminho_banco} estabelecida com sucesso.")
        return conexao
    except sqlite3.Error as erro:
        print(f"Erro ao conectar ao banco: {erro}")
        return None

def fechar_conexao(conexao):
    if conexao:
        conexao.close()
        print("Conexão fechada com sucesso.")


caminho_banco = "DB_seguradora"
conexao = conectar_banco(caminho_banco)


fechar_conexao(conexao)
