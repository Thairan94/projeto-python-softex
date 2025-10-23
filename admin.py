# admin.py
# Importa classes do PyQt6 para a interface:
# QWidget (janela base), QVBoxLayout (layout vertical), QPushButton (botão), QLabel (rótulo).
# QTableWidget (tabela para exibir dados), QTableWidgetItem (item para preencher a tabela).
# QHBoxLayout (layout horizontal para centralizar o botão), QMessageBox (caixa de diálogo).
# QHeaderView (cabeçalho da tabela), QAbstractItemView (controle de edição da tabela).
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox, QHeaderView, QAbstractItemView
# Importa a classe Qt para acessar constantes (como alinhamento).
from PyQt6.QtCore import Qt
# Importa QCursor para definir o ícone do mouse (mãozinha).
from PyQt6.QtGui import QCursor
# Importa as funções do banco: buscar usuários com reservas e deletar usuário.
from banco import listar_usuarios_com_reservas, deletar_usuario 

# Define a classe AppAdminUsuarios, a janela de administração.
class AppAdminUsuarios(QWidget):
    # Construtor da classe. Recebe a janela anterior (Login).
    def __init__(self, janela_anterior):
        # Chama o construtor da classe base (QWidget).
        super().__init__()
        # Armazena a referência à janela anterior (para fechar a tela admin).
        self.janela_anterior = janela_anterior
        # Define o título da janela.
        self.setWindowTitle("Área de Administração - Gerenciamento de Usuários")
        # Define a posição e o tamanho inicial da janela (800x500 para a tabela).
        self.setGeometry(100, 100, 800, 500) 
        # Aplica estilo CSS básico à janela.
        self.setStyleSheet("QWidget { background-color: #f0f0f0; font-family: Arial; }")

        # Chama os métodos para montar a interface.
        self.criar_interface()
        # Carrega os dados dos usuários na tabela assim que a janela abre.
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

        # Configura o número de colunas da tabela: 5 colunas.
        # As colunas são: Nome, Matrícula, Senha (Hash), Reservas Ativas, Ação.
        self.tabela_usuarios.setColumnCount(5)
        # Define os cabeçalhos das colunas.
        self.tabela_usuarios.setHorizontalHeaderLabels(["Nome", "Matrícula", "Senha (Hash)", "Reservas Ativas", "Ação"])
        
        # --- Configuração de Redimensionamento das Colunas ---
        header = self.tabela_usuarios.horizontalHeader()
        # Colunas 0, 1, 2 (Dados Pessoais/Hash) se ajustam ao conteúdo para ficarem compactas.
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        # Coluna 3 (Reservas) Ocupa o resto do espaço disponível (Stretch).
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        # Coluna 4 (Ação/Botão) se ajusta ao tamanho do botão.
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        
        # Permite apenas a leitura das células (não permite edição direta na tabela).
        self.tabela_usuarios.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

    # Método para buscar os usuários no banco de dados e preencher a tabela.
    def carregar_usuarios(self):
        # Limpa todas as linhas existentes na tabela antes de recarregar.
        self.tabela_usuarios.setRowCount(0)
        # Chama a função do banco para listar usuários e suas reservas.
        usuarios = listar_usuarios_com_reservas()
        
        # Define o número de linhas da tabela com base no número de usuários retornados.
        self.tabela_usuarios.setRowCount(len(usuarios))

        # Itera sobre a lista de usuários e seus índices (linha).
        for linha, usuario in enumerate(usuarios):
            # Obtém a matrícula do usuário.
            matricula = usuario['matricula']
            
            # Coluna 0: Nome
            self._set_table_item(linha, 0, usuario.get('nome', 'N/A'))

            # Coluna 1: Matrícula
            self._set_table_item(linha, 1, matricula)

            # Coluna 2: Senha (Hash)
            senha_hash_display = usuario.get('senha_hash', 'N/A')
            self._set_table_item(linha, 2, senha_hash_display) 

            # Coluna 3: Reservas Ativas (Texto formatado)
            reservas_str = usuario.get('reservas_ativas', 'Nenhuma reserva ativa')
            reservas_item = QTableWidgetItem(reservas_str)
            # Alinha o texto das reservas ao topo e à esquerda.
            reservas_item.setTextAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
            reservas_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            self.tabela_usuarios.setItem(linha, 3, reservas_item)
            
            # Ajusta a altura da linha para acomodar todo o texto das reservas.
            self.tabela_usuarios.resizeRowToContents(linha)
            
            # Coluna 4: Botão de Ação (Excluir)
            
            # Cria um QWidget container para a célula.
            widget_container = QWidget()
            # Cria um layout horizontal para centralizar o botão.
            h_layout = QHBoxLayout(widget_container)
            # Remove as margens internas do layout horizontal.
            h_layout.setContentsMargins(0, 0, 0, 0) 

            # Cria o botão de exclusão.
            botao_excluir = QPushButton("Excluir")
            # Estiliza o botão, definindo um padding compacto (4px superior/inferior, 8px laterais).
            botao_excluir.setStyleSheet("QPushButton { background-color: #F44336; color: white; border-radius: 4px; padding: 4px 8px; } QPushButton:hover { background-color: #D32F2F; }")
            botao_excluir.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            # Conecta o clique ao método excluir_usuario.
            botao_excluir.clicked.connect(lambda _, m=matricula: self.excluir_usuario(m))
            
            # Adiciona o botão ao layout horizontal, forçando a centralização vertical e horizontal.
            h_layout.addWidget(botao_excluir, alignment=Qt.AlignmentFlag.AlignCenter)
            
            # Insere o container (que contém o botão centralizado) na célula da tabela.
            self.tabela_usuarios.setCellWidget(linha, 4, widget_container)

    # Método auxiliar para configurar itens da tabela (para Nome, Matrícula, Senha)
    def _set_table_item(self, row, col, text):
        # Cria um novo item de tabela com o texto.
        item = QTableWidgetItem(text)
        # Define que o item é selecionável mas não editável.
        item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
        # Define o alinhamento centralizado para o texto.
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter) 
        # Insere o item na posição especificada.
        self.tabela_usuarios.setItem(row, col, item)

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
                # Exibe mensagem de sucesso.
                QMessageBox.information(self, "Sucesso", mensagem)
                # Recarrega a tabela para refletir a exclusão.
                self.carregar_usuarios()
            else:
                # Exibe mensagem de erro.
                QMessageBox.critical(self, "Erro", mensagem)

    # Sobrescreve o evento de fechar a janela.
    def closeEvent(self, event):
        # Ao fechar a janela de administração, re-exibe a janela de login.
        self.janela_anterior.show()
        # Permite que o evento de fechamento prossiga.
        event.accept()
