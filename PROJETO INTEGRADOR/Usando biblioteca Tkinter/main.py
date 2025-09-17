# main.py

# Importa a biblioteca Tkinter para criar a interface gráfica.
import tkinter as tk
# Importa a classe AppLogin do arquivo login.py.
from telaLogin import AppLogin

# Este bloco de código garante que o programa será executado apenas se
# for o arquivo principal (e não se for importado).
if __name__ == "__main__":
    # Cria a janela principal da aplicação.
    root = tk.Tk()
    # Inicia a aplicação instanciando a classe AppLogin.
    # Esta será a primeira tela a ser exibida.
    app = AppLogin(root)
    # Inicia o loop principal da interface gráfica. Ele mantém a janela aberta
    # e espera por eventos (como cliques do mouse).
    root.mainloop()
