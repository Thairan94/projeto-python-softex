# login.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QInputDialog, QLineEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from cadastro import AppCadastro
from reserva import AppReservaSalas
from DadosUsuarios import usuarios_cadastrados

class AppLogin(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Acesso ao Sistema")
        self.setGeometry(100, 100, 300, 200)
        self.setStyleSheet("QWidget { background-color: #f0f0f0; font-family: Arial; }")

        self.criar_interface()

    def criar_interface(self):
        layout_principal = QVBoxLayout()
        layout_principal.setSpacing(10)
        self.setLayout(layout_principal)

        titulo = QLabel("Bem-vindo(a)!")
        titulo.setStyleSheet("font-size: 19px; font-weight: bold; color: #333;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(titulo)

        botao_cadastrar = QPushButton("Cadastrar")
        botao_cadastrar.setFixedHeight(40)
        botao_cadastrar.setStyleSheet("QPushButton { background-color: #2196F3; color: white; border-radius: 5px; font-size: 18px; } QPushButton:hover { background-color: #1976D2; }")
        botao_cadastrar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        botao_cadastrar.clicked.connect(self.abrir_tela_cadastro)
        layout_principal.addWidget(botao_cadastrar)

        botao_entrar = QPushButton("Entrar")
        botao_entrar.setFixedHeight(40)
        botao_entrar.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; border-radius: 5px; font-size: 18px; } QPushButton:hover { background-color: #45a049; }")
        botao_entrar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        botao_entrar.clicked.connect(self.fazer_login)
        layout_principal.addWidget(botao_entrar)

    def abrir_tela_cadastro(self):
        self.hide()
        self.janela_cadastro = AppCadastro(self)
        self.janela_cadastro.show()

    def fazer_login(self):
        matricula, ok = QInputDialog.getText(self, "Login", "Digite sua matrícula:")
        if ok and matricula and matricula in usuarios_cadastrados:
            senha, ok = QInputDialog.getText(self, "Login", "Digite sua senha:", QLineEdit.EchoMode.Password)
            if ok and senha == usuarios_cadastrados[matricula]["senha"]:
                nome_usuario = usuarios_cadastrados[matricula]["nome"]
                self.hide()
                self.janela_reservas = AppReservaSalas(self, nome_usuario)
                self.janela_reservas.show()
            else:
                QMessageBox.critical(self, "Erro", "Senha incorreta.")
        else:
            QMessageBox.critical(self, "Erro", "Matrícula não encontrada.")
