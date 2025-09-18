# cadastro.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QCursor
from DadosUsuarios import usuarios_cadastrados

class AppCadastro(QWidget):
    def __init__(self, janela_anterior):
        super().__init__()
        self.janela_anterior = janela_anterior
        self.setWindowTitle("Cadastro de Usuário")
        self.setGeometry(100, 100, 350, 250)
        self.setStyleSheet("QWidget { background-color: #f0f0f0; font-family: Arial; }")

        self.criar_interface()

    def criar_interface(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        nome_label = QLabel("Nome:")
        nome_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(nome_label)
        self.nome_entry = QLineEdit()
        self.nome_entry.setStyleSheet("padding: 5px;")
        layout.addWidget(self.nome_entry)

        
        matricula_label = QLabel("Matricula:")
        matricula_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(matricula_label)
        self.matricula_entry = QLineEdit()
        self.matricula_entry.setStyleSheet("padding: 5px;")
        layout.addWidget(self.matricula_entry)

        
        senha_label = QLabel("Senha:")
        senha_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(senha_label)
        self.senha_entry = QLineEdit()
        self.senha_entry.setEchoMode(QLineEdit.EchoMode.Password)
        self.senha_entry.setStyleSheet("padding: 5px;")
        layout.addWidget(self.senha_entry)

        botao_salvar = QPushButton("Salvar")
        botao_salvar.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; border-radius: 5px; font-size: 14px; padding: 12px; margin-top: 10px; } QPushButton:hover { background-color: #45a049; }")
        botao_salvar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        botao_salvar.clicked.connect(self.salvar_cadastro)
        layout.addWidget(botao_salvar)
    
    def salvar_cadastro(self):
        nome = self.nome_entry.text()
        matricula = self.matricula_entry.text()
        senha = self.senha_entry.text()

        if not nome or not matricula or not senha:
            QMessageBox.critical(self, "Erro", "Por favor, preencha todos os campos.")
            return

        if not matricula.isdigit():
            QMessageBox.critical(self, "Erro de Validação", "A matrícula deve conter apenas números.")
            return

        if not senha.isalnum():
            QMessageBox.critical(self, "Erro de Validação", "A senha deve conter apenas letras e números, sem espaços ou caracteres especiais.")
            return

        if len(senha) < 8:
            QMessageBox.critical(self, "Erro de Validação", "A senha deve ter no mínimo 8 caracteres.")
            return
            
        if matricula in usuarios_cadastrados:
            QMessageBox.critical(self, "Erro", "Matrícula já cadastrada!")
        else:
            usuarios_cadastrados[matricula] = {"nome": nome, "senha": senha}
            QMessageBox.information(self, "Sucesso", "Usuário cadastrado com sucesso!")
            self.janela_anterior.show()
            self.close()
