# main.py
# Importa a QApplication para gerenciar a aplicação PyQt
from PyQt6.QtWidgets import QApplication
# Importa a janela de Login, que é o ponto de partida
from login import AppLogin
# Importa o módulo do banco de dados (A função inicializar_banco() é chamada na importação)
import banco 
import sys

if __name__ == "__main__":
    # Cria a instância da aplicação
    app = QApplication(sys.argv)
    
    # Cria a janela de Login
    janela_login = AppLogin()
    # Exibe a janela de Login
    janela_login.show()
    
    # Inicia o loop de eventos da aplicação, mantendo a janela aberta
    sys.exit(app.exec())
