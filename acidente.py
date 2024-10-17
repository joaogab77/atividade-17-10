import tkinter as tk
from tkinter import messagebox
import sqlite3
import re

# Função para conectar ao banco de dados
def conectar_banco():
    try:
        conexao = sqlite3.connect('meu_banco.db')  # Certifique-se que o nome do banco esteja correto
        return conexao
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para validação de campos
def validar_campos_usuario():
    if not entry_codigo.get().isdigit():
        messagebox.showerror("Erro", "O campo 'Código' deve ser um número inteiro.")
        return False
    if not entry_nome.get():
        messagebox.showerror("Erro", "O campo 'Nome' não pode estar vazio.")
        return False
    if not entry_username.get():
        messagebox.showerror("Erro", "O campo 'Username' não pode estar vazio.")
        return False
    if not entry_senha.get():
        messagebox.showerror("Erro", "O campo 'Senha' não pode estar vazio.")
        return False
    return True

# Funções de operações com a tabela tbl_usuarios
def inserir_usuario():
    if not validar_campos_usuario():
        return
    with conectar_banco() as conexao:
        cursor = conexao.cursor()
        try:
            cursor.execute("""
                INSERT INTO tbl_usuarios (usu_codigo, usu_nome, usu_username, usu_senha)
                VALUES (?, ?, ?, ?)
            """, (entry_codigo.get(), entry_nome.get(), entry_username.get(), entry_senha.get()))
            conexao.commit()
            messagebox.showinfo("Sucesso", "Usuário inserido com sucesso")
            limpar_campos_usuario()
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao inserir usuário: {e}")

def alterar_usuario():
    if not validar_campos_usuario():
        return
    with conectar_banco() as conexao:
        cursor = conexao.cursor()
        try:
            cursor.execute("""
                UPDATE tbl_usuarios SET 
                    usu_nome = ?, usu_username = ?, usu_senha = ?
                WHERE usu_codigo = ?
            """, (entry_nome.get(), entry_username.get(), entry_senha.get(), entry_codigo.get()))
            conexao.commit()
            if cursor.rowcount == 0:
                messagebox.showinfo("Alteração", "Nenhum usuário foi alterado.")
            else:
                messagebox.showinfo("Sucesso", "Usuário alterado com sucesso")
                limpar_campos_usuario()
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao alterar usuário: {e}")

def excluir_usuario():
    if not entry_codigo.get().isdigit():
        messagebox.showerror("Erro", "O campo 'Código' deve ser um número inteiro.")
        return
    with conectar_banco() as conexao:
        cursor = conexao.cursor()
        try:
            cursor.execute("DELETE FROM tbl_usuarios WHERE usu_codigo = ?", (entry_codigo.get(),))
            conexao.commit()
            if cursor.rowcount == 0:
                messagebox.showinfo("Exclusão", "Nenhum usuário foi excluído.")
            else:
                messagebox.showinfo("Sucesso", "Usuário excluído com sucesso")
                limpar_campos_usuario()
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao excluir usuário: {e}")

def consultar_usuario():
    if not entry_codigo.get().isdigit():
        messagebox.showerror("Erro", "O campo 'Código' deve ser um número inteiro.")
        return
    with conectar_banco() as conexao:
        cursor = conexao.cursor()
        try:
            cursor.execute("SELECT * FROM tbl_usuarios WHERE usu_codigo = ?", (entry_codigo.get(),))
            usuario = cursor.fetchone()
            if usuario:
                entry_nome.delete(0, tk.END)
                entry_nome.insert(0, usuario[1])
                entry_username.delete(0, tk.END)
                entry_username.insert(0, usuario[2])
                entry_senha.delete(0, tk.END)
                entry_senha.insert(0, usuario[3])
            else:
                messagebox.showinfo("Consulta", "Usuário não encontrado")
                limpar_campos_usuario()
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao consultar usuário: {e}")

# Função para limpar os campos após operações
def limpar_campos_usuario():
    entry_codigo.delete(0, tk.END)
    entry_nome.delete(0, tk.END)
    entry_username.delete(0, tk.END)
    entry_senha.delete(0, tk.END)

# Interface gráfica para a tela de usuários
def criar_tela_usuario():
    janela = tk.Tk()
    janela.title("Manutenção de Usuários")

    # Labels e campos de entrada
    tk.Label(janela, text="Código:").grid(row=0, column=0)
    global entry_codigo
    entry_codigo = tk.Entry(janela)
    entry_codigo.grid(row=0, column=1)

    tk.Label(janela, text="Nome:").grid(row=1, column=0)
    global entry_nome
    entry_nome = tk.Entry(janela)
    entry_nome.grid(row=1, column=1)

    tk.Label(janela, text="Username:").grid(row=2, column=0)
    global entry_username
    entry_username = tk.Entry(janela)
    entry_username.grid(row=2, column=1)

    tk.Label(janela, text="Senha:").grid(row=3, column=0)
    global entry_senha
    entry_senha = tk.Entry(janela)
    entry_senha.grid(row=3, column=1)

    # Botões de operações
    btn_inserir = tk.Button(janela, text="Incluir", command=inserir_usuario)
    btn_inserir.grid(row=4, column=0)

    btn_alterar = tk.Button(janela, text="Alterar", command=alterar_usuario)
    btn_alterar.grid(row=4, column=1)

    btn_excluir = tk.Button(janela, text="Excluir", command=excluir_usuario)
    btn_excluir.grid(row=5, column=0)

    btn_consultar = tk.Button(janela, text="Consultar", command=consultar_usuario)
    btn_consultar.grid(row=5, column=1)

    janela.mainloop()

# Chama a função para criar a tela de manutenção de usuários
criar_tela_usuario()
