# login.py
import tkinter as tk
from tkinter import messagebox, simpledialog
from telaCadastro import AppCadastro
from telaReserva import AppReservaSalas
from dados_usuarios import usuarios_cadastrados

class AppLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Acesso ao Sistema")
        self.root.geometry("300x200")
        self.root.configure(bg="#f0f0f0")
        self.criar_interface()

    def criar_interface(self):
        frame_principal = tk.Frame(self.root, bg="#f0f0f0", padx=20, pady=20)
        frame_principal.pack(expand=True)
        titulo = tk.Label(frame_principal, text="Bem-vindo(a)!", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333")
        titulo.pack(pady=10)

        botao_cadastrar = tk.Button(frame_principal, text="Cadastrar", font=("Arial", 12), width=15, height=1,
                                    bg="#2196F3", fg="white", activebackground="#1976D2", cursor="hand2",
                                    command=self.abrir_tela_cadastro)
        botao_cadastrar.pack(pady=5)

        botao_entrar = tk.Button(frame_principal, text="Entrar", font=("Arial", 12), width=15, height=1,
                                 bg="#4CAF50", fg="white", activebackground="#45a049", cursor="hand2",
                                 command=self.fazer_login)
        botao_entrar.pack(pady=5)

    def abrir_tela_cadastro(self):
        self.root.withdraw()
        janela_cadastro = tk.Toplevel(self.root)
        AppCadastro(janela_cadastro, self.root)

    def fazer_login(self):
        matricula = simpledialog.askstring("Login", "Digite sua matrícula:")
        if matricula and matricula in usuarios_cadastrados:
            senha = simpledialog.askstring("Login", "Digite sua senha:", show='*')
            if senha == usuarios_cadastrados[matricula]["senha"]:
                nome_usuario = usuarios_cadastrados[matricula]["nome"]
                self.root.withdraw()
                janela_reservas = tk.Toplevel(self.root)
                AppReservaSalas(janela_reservas, self.root, nome_usuario)
            else:
                messagebox.showerror("Erro", "Senha incorreta.")
        else:
            messagebox.showerror("Erro", "Matrícula não encontrada.")
