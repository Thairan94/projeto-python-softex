# reserva.py
import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime

class AppReservaSalas:
    def __init__(self, root, janela_anterior, nome_usuario):
        self.root = root
        self.janela_anterior = janela_anterior
        self.nome_usuario = nome_usuario
        self.root.title("Sistema de Reserva de Salas")
        self.root.geometry("400x350")
        self.root.configure(bg="#f0f0f0")
        
        self.salas = {
            "Biblioteca": None,
            "Informática": None,
            "Robótica": None,
            "Ciências": None 
        }
        
        self.botoes = {}
        self.criar_interface()
        self.atualizar_interface()

    def criar_interface(self):
        frame_principal = tk.Frame(self.root, bg="#f0f0f0", padx=20, pady=20)
        frame_principal.pack(expand=True)

        titulo = tk.Label(frame_principal, text=f"Bem-vindo(a), {self.nome_usuario}!", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333")
        titulo.pack(pady=(0, 15))
        titulo = tk.Label(frame_principal, text=f"Escolha a sala:", font=("Arial", 14, "bold"), bg="#f0f0f0", fg="#333")
        titulo.pack(pady=(0, 15))

        for sala in self.salas:
            botao = tk.Button(frame_principal, text=f"Reservar {sala}", 
                              font=("Arial", 12), width=25, height=2,
                              relief=tk.RAISED, bd=2, cursor="hand2",
                              command=lambda s=sala: self.reservar_sala(s))
            botao.pack(pady=10)
            self.botoes[sala] = botao

    def atualizar_interface(self):
        for sala, status in self.salas.items():
            botao = self.botoes[sala]
            if status is None:
                botao.config(text=f"Reservar {sala}", bg="#4CAF50", fg="white", activebackground="#45a049")
            else:
                botao.config(text=f"Sala {sala} - Ocupada", bg="#F44336", fg="white", activebackground="#D32F2F")
    
    def reservar_sala(self, sala):
        info_reserva = self.salas[sala]

        if info_reserva is not None:
            mensagem = (f"A sala {sala} já está reservada!\n\n"
                        f"Reservado por: {info_reserva['nome']}\n"
                        f"Horário: {info_reserva['horario']}")
            messagebox.showerror("Sala Indisponível", mensagem)
        else:
            horario_atual = datetime.now().strftime("%H:%M:%S em %d/%m/%Y")
            self.salas[sala] = {
                "nome": self.nome_usuario,
                "horario": horario_atual
            }
            
            messagebox.showinfo("Sucesso!", f"A sala {sala} foi reservada por {self.nome_usuario}!")
            self.atualizar_interface()
