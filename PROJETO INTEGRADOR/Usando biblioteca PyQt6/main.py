# main.py

# Importa a biblioteca principal do PyQt6.
import sys
from PyQt6.QtWidgets import QApplication
# Importa a classe AppLogin do arquivo login.py.
from login import AppLogin

# Este bloco de código garante que o programa será executado apenas se
# for o arquivo principal (e não se for importado).
if __name__ == "__main__":
    # Cria a aplicação PyQt6.
    app = QApplication(sys.argv)
    # Inicia a aplicação instanciando a classe AppLogin.
    ex = AppLogin()
    # Exibe a janela principal.
    ex.show()
    # Inicia o loop principal da interface gráfica.
    sys.exit(app.exec())
