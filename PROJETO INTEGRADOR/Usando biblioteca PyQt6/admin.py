# admin.py

# Importa classes do PyQt6 para a interface:
# QWidget (janela base), QVBoxLayout (layout vertical), QPushButton (botão), QLabel (rótulo).
# QTableWidget (tabela para exibir dados), QTableWidgetItem (item para preencher a tabela).
# QHBoxLayout (layout horizontal), QMessageBox (caixa de diálogo de mensagem).
# QHeaderView (para configurar a largura das colunas da tabela).
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox, QHeaderView
# Importa a classe Qt para acessar constantes.
from PyQt6.QtCore import Qt
# Importa QCursor para definir o ícone do mouse.
from PyQt6.QtGui import QCursor
# Importa as funções de gerenciamento de usuários do banco de dados (SQLite).
from banco import listar_usuarios, deletar_usuario

# Define a classe AppAdminUsuarios, a janela de administração.
class AppAdminUsuarios(QWidget):
    # Construtor da classe. Recebe a janela anterior (Login).
    def __init__(self, janela_anterior):
        # Chama o construtor da classe base (QWidget).
        super().__init__()
        # Armazena a referência à janela anterior.
        self.janela_anterior = janela_anterior
        # Define o título da janela.
        self.setWindowTitle("Área de Administração - Gerenciamento de Usuários")
        # Define a posição e o tamanho inicial da janela.
        self.setGeometry(100, 100, 600, 400)
        # Aplica estilo CSS básico à janela.
        self.setStyleSheet("QWidget { background-color: #f0f0f0; font-family: Arial; }")

        # Chama os métodos para montar a interface.
        self.criar_interface()
        # Carrega os dados dos usuários na tabela.
        self.carregar_usuarios()

    # Método para montar o layout visual.
    def criar_interface(self):
        # Cria um layout vertical principal.
        layout = QVBoxLayout()
        # Aplica o layout à janela.
        self.setLayout(layout)

        # Cria e estiliza o rótulo do título.
        titulo = QLabel("Gerenciamento de Usuários")
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: #333;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Adiciona o título ao layout.
        layout.addWidget(titulo)

        # Cria o widget de tabela (QTableWidget).
        self.tabela_usuarios = QTableWidget()
        # Adiciona a tabela ao layout.
        layout.addWidget(self.tabela_usuarios)

        # Configura o número de colunas da tabela: Nome, Matrícula, Senha, Ação (Botão).
        self.tabela_usuarios.setColumnCount(4)
        # Define os cabeçalhos das colunas.
        self.tabela_usuarios.setHorizontalHeaderLabels(["Nome", "Matrícula", "Senha", "Ação"])
        
        # Ajusta a largura das colunas para preencher o espaço disponível.
        self.tabela_usuarios.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # Define a coluna 'Ação' para ter um tamanho fixo (melhora o visual dos botões).
        self.tabela_usuarios.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)

    # Método para buscar os usuários no banco de dados e preencher a tabela.
    def carregar_usuarios(self):
        # Limpa todas as linhas existentes na tabela antes de carregar novas.
        self.tabela_usuarios.setRowCount(0)
        # Chama a função do banco para listar todos os usuários.
        usuarios = listar_usuarios()
        
        # Define o número de linhas da tabela com base no número de usuários.
        self.tabela_usuarios.setRowCount(len(usuarios))

        # Itera sobre a lista de usuários e seus índices.
        for linha, usuario in enumerate(usuarios):
            # Obtém a matrícula do usuário para usar na exclusão.
            matricula = usuario['matricula']
            
            # --- Preenchimento das Células ---
            
            # Coluna 0: Nome
            nome_item = QTableWidgetItem(usuario['nome'])
            # Desabilita a edição da célula.
            nome_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            self.tabela_usuarios.setItem(linha, 0, nome_item)

            # Coluna 1: Matrícula
            matricula_item = QTableWidgetItem(matricula)
            matricula_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            self.tabela_usuarios.setItem(linha, 1, matricula_item)

            # Coluna 2: Senha (exibida em texto simples, pois é uma tela administrativa)
            senha_item = QTableWidgetItem(usuario['senha'])
            senha_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            self.tabela_usuarios.setItem(linha, 2, senha_item)
            
            # Coluna 3: Botão de Ação
            # Cria um botão de exclusão.
            botao_excluir = QPushButton("Excluir")
            # Estiliza o botão com cor vermelha.
            botao_excluir.setStyleSheet("QPushButton { background-color: #F44336; color: white; border-radius: 4px; padding: 5px; } QPushButton:hover { background-color: #D32F2F; }")
            # Conecta o clique do botão ao método de exclusão, passando a matrícula.
            botao_excluir.clicked.connect(lambda _, m=matricula: self.excluir_usuario(m))
            
            # Adiciona o botão na célula da tabela.
            self.tabela_usuarios.setCellWidget(linha, 3, botao_excluir)

    # Método para deletar um usuário do sistema.
    def excluir_usuario(self, matricula):
        # Exibe uma caixa de diálogo de confirmação.
        resposta = QMessageBox.question(self, "Confirmar Exclusão",
                                        f"Tem certeza que deseja excluir o usuário com a matrícula {matricula}?",
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        # Se o administrador confirmar...
        if resposta == QMessageBox.StandardButton.Yes:
            # Chama a função do banco para deletar o usuário e suas reservas.
            sucesso, mensagem = deletar_usuario(matricula)
            
            if sucesso:
                # Se a exclusão for bem-sucedida, exibe a mensagem de sucesso.
                QMessageBox.information(self, "Sucesso", mensagem)
                # Recarrega a tabela para refletir a exclusão.
                self.carregar_usuarios()
            else:
                # Se houver erro, exibe a mensagem de erro retornada pelo banco.
                QMessageBox.critical(self, "Erro", mensagem)

    # Sobrescreve o evento de fechar a janela.
    def closeEvent(self, event):
        # Quando a janela de administração é fechada, re-exibe a janela de login.
        self.janela_anterior.show()
        # Permite que o evento de fechamento da janela ocorra.
        event.accept()
