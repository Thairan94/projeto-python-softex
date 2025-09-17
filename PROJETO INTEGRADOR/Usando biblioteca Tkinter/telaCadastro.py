# cadastro.py
import tkinter as tk
from tkinter import messagebox, simpledialog
from dados_usuarios import usuarios_cadastrados

class AppCadastro:
    def __init__(self, root, janela_anterior):
        self.root = root
        self.janela_anterior = janela_anterior
        self.root.title("Cadastro de Usuário")
        self.root.geometry("350x250")
        self.root.configure(bg="#f0f0f0")
        self.criar_interface()

    def criar_interface(self):
        frame = tk.Frame(self.root, bg="#f0f0f0", padx=20, pady=20)
        frame.pack(expand=True)
        
        tk.Label(frame, text="Nome:", bg="#f0f0f0").pack()
        self.nome_entry = tk.Entry(frame)
        self.nome_entry.pack()

        tk.Label(frame, text="Matrícula:", bg="#f0f0f0").pack()
        self.matricula_entry = tk.Entry(frame)
        self.matricula_entry.pack()

        tk.Label(frame, text="Senha:", bg="#f0f0f0").pack()
        vcmd = (self.root.register(self.validar_senha), '%P')
        self.senha_entry = tk.Entry(frame, show="*", validate="key", validatecommand=vcmd)
        self.senha_entry.pack()
        
        botao_salvar = tk.Button(frame, text="Salvar", command=self.salvar_cadastro)
        botao_salvar.pack(pady=10)

    def validar_senha(self, p):
        return len(p) <= 8
        
    def salvar_cadastro(self):
        nome = self.nome_entry.get()
        matricula = self.matricula_entry.get()
        senha = self.senha_entry.get()

        if not matricula.isdigit():
            messagebox.showerror("Erro de Validação", "A matrícula deve conter apenas números.")
            return

        if not senha.isalnum():
            messagebox.showerror("Erro de Validação", "A senha deve conter apenas letras e números, sem espaços ou caracteres especiais.")
            return
        
        if len(senha) < 8:
            messagebox.showerror("Erro de Validação", "A senha deve ter no mínimo 8 caracteres.")
            return

        if nome and matricula and senha:
            if matricula in usuarios_cadastrados:
                messagebox.showerror("Erro", "Matrícula já cadastrada!")
            else:
                usuarios_cadastrados[matricula] = {"nome": nome, "senha": senha}
                messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
                self.root.destroy()
                self.janela_anterior.deiconify()
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
