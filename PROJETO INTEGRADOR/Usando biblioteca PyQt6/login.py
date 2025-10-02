# login.py
# Importa classes do PyQt6 para a interface:
# QWidget (janela base), QVBoxLayout (layout vertical), QPushButton (botão), QLabel (rótulo/texto),
# QMessageBox (caixa de diálogo de mensagem), QInputDialog (caixa de diálogo para entrada de dados),
# QLineEdit (campo de entrada de texto).
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QInputDialog, QLineEdit
# Importa Qt para constantes (ex: centralização).
from PyQt6.QtCore import Qt, QByteArray
# Importa QCursor para definir o ícone do mouse (mãozinha).
from PyQt6.QtGui import QCursor, QPixmap
# Importa as classes das outras telas para navegação.
from cadastro import AppCadastro
from reserva import AppReservaSalas
from admin import AppAdminUsuarios  # Importa a nova tela de administração
from banco import verificar_login 

# Define a classe AppLogin que representa a janela de login.
class AppLogin(QWidget):
    # Construtor da classe.
    def __init__(self):
        # Chama o construtor da classe pai (QWidget).
        super().__init__()
        # Define o título da janela.
        self.setWindowTitle("Acesso ao Sistema")
        # Define a posição e o tamanho da janela.
        self.setGeometry(100, 100, 300, 200)
        # Aplica estilo CSS básico à janela.
        self.setStyleSheet("QWidget { background-color: #f0f0f0; font-family: Arial; }")

        # Chama o método para construir os elementos da interface.
        self.criar_interface()

    # Método responsável por montar o layout visual.
    def criar_interface(self):
        # Cria um layout vertical para organizar os widgets.
        layout_principal = QVBoxLayout()
        # Define o espaçamento entre os widgets.
        layout_principal.setSpacing(10)
        # Aplica o layout à janela.
        self.setLayout(layout_principal)

        # Cria o rótulo de boas-vindas.
        titulo = QLabel("Bem-vindo(a)!")
        # Aplica estilo CSS ao título.
        titulo.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        # Centraliza o texto do rótulo.
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Adiciona o título ao layout.
        layout_principal.addWidget(titulo)

       
        

        # Cria o botão Cadastrar.
        botao_cadastrar = QPushButton("Cadastrar")
        # Define a altura fixa do botão.
        botao_cadastrar.setFixedHeight(40)
        # Aplica estilo CSS ao botão Cadastrar (azul) e aumenta a fonte.
        botao_cadastrar.setStyleSheet("QPushButton { background-color: #2196F3; color: white; border-radius: 5px; font-size: 18px; } QPushButton:hover { background-color: #1976D2; }")
        # Define o cursor como uma mãozinha.
        botao_cadastrar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        # Conecta o clique do botão ao método que abre a tela de cadastro.
        botao_cadastrar.clicked.connect(self.abrir_tela_cadastro)
        # Adiciona o botão ao layout.
        layout_principal.addWidget(botao_cadastrar)

        # Cria o botão Entrar.
        botao_entrar = QPushButton("Entrar")
        # Define a altura fixa do botão.
        botao_entrar.setFixedHeight(40)
        # Aplica estilo CSS ao botão Entrar (verde) e aumenta a fonte.
        botao_entrar.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; border-radius: 5px; font-size: 18px; } QPushButton:hover { background-color: #45a049; }")
        # Define o cursor como uma mãozinha.
        botao_entrar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        # Conecta o clique do botão ao método que faz o login.
        botao_entrar.clicked.connect(self.fazer_login)
        # Adiciona o botão ao layout.
        layout_principal.addWidget(botao_entrar)

    # Método para iniciar a tela de cadastro.
    def abrir_tela_cadastro(self):
        # Esconde a janela atual (login).
        self.hide()
        # Cria uma nova instância da janela de Cadastro.
        self.janela_cadastro = AppCadastro(self)
        # Exibe a janela de cadastro.
        self.janela_cadastro.show()

    # Método para processar a tentativa de login.
    def fazer_login(self):
        # Abre uma caixa de diálogo para pedir a matrícula.
        matricula, ok = QInputDialog.getText(self, "Login", "Digite sua matrícula:")
        # Verifica se o usuário clicou em OK e se a matrícula não está vazia.
        if ok and matricula:
            # Abre uma caixa de diálogo para pedir a senha, usando o modo Password para ocultar o texto.
            senha, ok = QInputDialog.getText(self, "Login", "Digite sua senha:", QLineEdit.EchoMode.Password)
            
            # **NOVA LÓGICA ADMIN:** Verifica credenciais especiais para acesso administrativo.
            if matricula == "admin" and senha == "12345678":
                self.hide()
                # Cria e exibe a janela de Administração.
                self.janela_admin = AppAdminUsuarios(self)
                self.janela_admin.show()
                return # Sai da função, pois o login admin foi bem-sucedido.

            # Tenta verificar as credenciais no banco de dados.
            usuario = verificar_login(matricula, senha)
            
            # Verifica se o usuário clicou em OK na senha E se o banco retornou um usuário válido.
            if ok and usuario:
                # Login normal bem-sucedido. Extrai o nome e a matrícula do dicionário retornado.
                nome_usuario = usuario['nome']
                matricula_usuario = usuario['matricula'] # Matrícula também é necessária para a reserva.
                # Esconde a janela de login.
                self.hide()
                # Cria e exibe a janela de Reserva de Salas, passando nome e matrícula.
                self.janela_reservas = AppReservaSalas(self, nome_usuario, matricula_usuario)
                self.janela_reservas.show()
            else:
                # Login normal falhou (matrícula ou senha incorreta).
                QMessageBox.critical(self, "Erro", "Matrícula ou senha incorreta.")
        else:
            # Usuário não inseriu a matrícula.
            QMessageBox.critical(self, "Erro", "A matrícula não pode ser vazia.")
