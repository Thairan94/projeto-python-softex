# cadastro.py
# Importa classes do PyQt6 para a interface:
# QWidget (janela base), QVBoxLayout (layout vertical), QPushButton (botão), QLabel (rótulo/texto),
# QLineEdit (campo de entrada de texto), QMessageBox (caixa de diálogo de mensagem).
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox
# Importa Qt para constantes (cursor).
from PyQt6.QtCore import Qt
# Importa QCursor para definir o ícone do mouse.
from PyQt6.QtGui import QCursor
# Importa a função de cadastro do banco de dados (SQLite), que faz a persistência.
from banco import cadastrar_usuario 

# Define a classe AppCadastro que herda de QWidget, criando a janela de cadastro.
class AppCadastro(QWidget):
    # Construtor da classe.
    def __init__(self, janela_anterior):
        # Chama o construtor da classe pai (QWidget).
        super().__init__()
        # Armazena a janela de login, permitindo voltar a ela após o cadastro.
        self.janela_anterior = janela_anterior
        # Define o título da janela.
        self.setWindowTitle("Cadastro de Usuário")
        # Define a posição e o tamanho da janela (largura x altura).
        self.setGeometry(100, 100, 350, 250)
        # Aplica estilo CSS básico à janela.
        self.setStyleSheet("QWidget { background-color: #f0f0f0; font-family: Arial; }")

        # Chama o método para construir a interface visual.
        self.criar_interface()

    # Método para montar o layout visual e os widgets.
    def criar_interface(self):
        # Cria um layout vertical para organizar os elementos.
        layout = QVBoxLayout()
        # Aplica o layout à janela.
        self.setLayout(layout)

        # --- Campo Nome ---
        # Cria o rótulo "Nome:".
        nome_label = QLabel("Nome:")
        # Aplica estilo à fonte do rótulo.
        nome_label.setStyleSheet("font-size: 14px;")
        # Adiciona o rótulo ao layout.
        layout.addWidget(nome_label)
        # Cria o campo de entrada para o nome.
        self.nome_entry = QLineEdit()
        # Aplica estilo para aumentar o padding (espaçamento interno) do campo.
        self.nome_entry.setStyleSheet("padding: 5px;")
        # Adiciona o campo ao layout.
        layout.addWidget(self.nome_entry)

        # --- Campo Matrícula ---
        # Cria o rótulo "Matricula:".
        matricula_label = QLabel("Matricula:")
        # Aplica estilo à fonte do rótulo.
        matricula_label.setStyleSheet("font-size: 14px;")
        # Adiciona o rótulo ao layout.
        layout.addWidget(matricula_label)
        # Cria o campo de entrada para a matrícula.
        self.matricula_entry = QLineEdit()
        # Aplica estilo para aumentar o padding.
        self.matricula_entry.setStyleSheet("padding: 5px;")
        # Adiciona o campo ao layout.
        layout.addWidget(self.matricula_entry)

        # --- Campo Senha ---
        # Cria o rótulo "Senha:".
        senha_label = QLabel("Senha:")
        # Aplica estilo à fonte do rótulo.
        senha_label.setStyleSheet("font-size: 14px;")
        # Adiciona o rótulo ao layout.
        layout.addWidget(senha_label)
        # Cria o campo de entrada para a senha.
        self.senha_entry = QLineEdit()
        # Define o modo de eco para ocultar o texto (mostra pontos).
        self.senha_entry.setEchoMode(QLineEdit.EchoMode.Password)
        # Aplica estilo para aumentar o padding.
        self.senha_entry.setStyleSheet("padding: 5px;")
        # Adiciona o campo ao layout.
        layout.addWidget(self.senha_entry)

        # --- Botão Salvar ---
        # Cria o botão "Salvar".
        botao_salvar = QPushButton("Salvar")
        # Aplica estilo CSS ao botão (cor, arredondamento, tamanho da fonte e margens).
        botao_salvar.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; border-radius: 5px; font-size: 14px; padding: 12px; margin-top: 10px; } QPushButton:hover { background-color: #45a049; }")
        # Define o cursor como uma mãozinha ao passar por cima.
        botao_salvar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        # Conecta o clique do botão ao método que processa o cadastro.
        botao_salvar.clicked.connect(self.salvar_cadastro)
        # Adiciona o botão ao layout.
        layout.addWidget(botao_salvar)
    
    # Método que processa a validação e o salvamento dos dados.
    def salvar_cadastro(self):
        # Obtém o texto atual de cada campo de entrada.
        nome = self.nome_entry.text()
        matricula = self.matricula_entry.text()
        senha = self.senha_entry.text()

        # 1. Validação de campos vazios.
        if not nome or not matricula or not senha:
            QMessageBox.critical(self, "Erro", "Por favor, preencha todos os campos.")
            return

        # 2. Validação: Matrícula deve conter apenas dígitos (números).
        if not matricula.isdigit():
            QMessageBox.critical(self, "Erro de Validação", "A matrícula deve conter apenas números.")
            return

        # 3. Validação: Senha deve ser alfanumérica (letras e números apenas).
        if not senha.isalnum():
            QMessageBox.critical(self, "Erro de Validação", "A senha deve conter apenas letras e números, sem espaços ou caracteres especiais.")
            return

        # 4. Validação: Senha deve ter no mínimo 8 caracteres.
        if len(senha) < 8:
            QMessageBox.critical(self, "Erro de Validação", "A senha deve ter no mínimo 8 caracteres.")
            return
            
        # 5. Tenta cadastrar o usuário no banco de dados SQLite.
        # A função cadastrar_usuario retorna uma tupla: (bool sucesso, str mensagem).
        sucesso, mensagem = cadastrar_usuario(matricula, nome, senha)

        if sucesso:
            # Se o cadastro foi bem-sucedido:
            QMessageBox.information(self, "Sucesso", mensagem)
            # Mostra a janela anterior (Login).
            self.janela_anterior.show()
            # Fecha a janela de cadastro.
            self.close()
        else:
            # Se o cadastro falhou (ex: matrícula duplicada):
            QMessageBox.critical(self, "Erro", mensagem)
