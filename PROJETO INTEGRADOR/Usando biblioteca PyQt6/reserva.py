from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from datetime import datetime

class AppReservaSalas(QWidget):
    def __init__(self, janela_anterior, nome_usuario):
        super().__init__()
        self.janela_anterior = janela_anterior
        self.nome_usuario = nome_usuario
        self.setWindowTitle("Sistema de Reserva de Salas")
        self.setGeometry(100, 100, 400, 350)
        self.setStyleSheet("QWidget { background-color: #f0f0f0; font-family: Arial; }")

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
        layout_principal = QVBoxLayout()
        layout_principal.setSpacing(10)
        self.setLayout(layout_principal)

        titulo = QLabel(f"Bem-vindo(a), {self.nome_usuario}!")
        titulo.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitulo = QLabel(f"Escolha a sala:")
        subtitulo.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(titulo)
        layout_principal.addWidget(subtitulo)

        for sala in self.salas:
            botao = QPushButton(f"Reservar {sala}")
            botao.setFixedHeight(50)
            botao.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; border-radius: 8px; font-size: 18px; } QPushButton:hover { background-color: #45a049; }")
            botao.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            botao.clicked.connect(lambda _, s=sala: self.reservar_sala(s))
            self.botoes[sala] = botao
            layout_principal.addWidget(botao)

    def criar_interface(self):
        layout_principal = QVBoxLayout()
        layout_principal.setSpacing(10)
        self.setLayout(layout_principal)

        titulo = QLabel(f"Bem-vindo(a), {self.nome_usuario}!")
        titulo.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(titulo)

        for sala in self.salas:
            botao = QPushButton(f"Reservar {sala}")
            botao.setFixedHeight(50)
            # Define o estilo inicial do botão, incluindo a fonte.
            botao.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50; 
                    color: white; 
                    border-radius: 8px; 
                    font-size: 18px; 
                }
                QPushButton:hover {
                    background-color: #45a049; 
                }
            """)
            botao.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            botao.clicked.connect(lambda _, s=sala: self.reservar_sala(s))
            self.botoes[sala] = botao
            layout_principal.addWidget(botao)

    def atualizar_interface(self):
        for sala, status in self.salas.items():
            botao = self.botoes[sala]
            if status is None:
                # Altera apenas a cor do botão, mantendo os outros estilos.
                botao.setStyleSheet("""
                    QPushButton {
                        background-color: #4CAF50; 
                        color: white; 
                        border-radius: 8px; 
                        font-size: 18px; 
                    }
                    QPushButton:hover {
                        background-color: #45a049; 
                    }
                """)
            else:
                # Altera a cor do botão para o estado 'ocupado'.
                botao.setText(f"Sala {sala} - Ocupada")
                botao.setStyleSheet("""
                    QPushButton {
                        background-color: #F44336; 
                        color: white; 
                        border-radius: 8px; 
                        font-size: 18px; 
                    }
                    QPushButton:hover {
                        background-color: #D32F2F; 
                    }
                """)
            
            botao.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def reservar_sala(self, sala):
        info_reserva = self.salas[sala]
        if info_reserva is not None:
            mensagem = (f"A sala {sala} já está reservada!\n\n"
                        f"Reservado por: {info_reserva['nome']}\n"
                        f"Horário: {info_reserva['horario']}")
            QMessageBox.warning(self, "Sala Indisponível", mensagem)
        else:
            horario_atual = datetime.now().strftime("%H:%M:%S em %d/%m/%Y")
            self.salas[sala] = {
                "nome": self.nome_usuario,
                "horario": horario_atual
            }
            QMessageBox.information(self, "Sucesso!", f"A sala {sala} foi reservada por {self.nome_usuario}!")
            self.atualizar_interface()