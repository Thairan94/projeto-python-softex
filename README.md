📅 Sistema de Reserva de Salas (Desktop Multi-Usuário)
Este projeto é um sistema de agendamento de salas desenvolvido em Python com PyQt6 para a interface gráfica e SQLite para persistência e sincronização de dados. O sistema implementa regras de negócio como limite de reservas por usuário e criptografia de senha (Bcrypt).

🚀 Como Rodar o Projeto
Siga os passos abaixo para configurar e executar o aplicativo em sua máquina.

1. Pré-requisitos
Você precisa ter o Python 3 instalado em seu sistema.

2. Instalação das Dependências
Abra seu terminal ou prompt de comando (PowerShell/CMD) e instale as bibliotecas necessárias: PyQt6 e Bcrypt.

pip install PyQt6 bcrypt

3. Estrutura do Projeto
Certifique-se de que todos os arquivos (main.py, login.py, banco.py, etc.) estão localizados na mesma pasta:

/SeuProjeto/
├── main.py
├── login.py
├── cadastro.py
├── reserva.py
├── admin.py
├── banco.py  <- Módulo de acesso ao Banco de Dados
└── reservas_salas.db  <- Arquivo do banco de dados (criado automaticamente)

4. Inicialização do Sistema
O arquivo main.py é o ponto de entrada do aplicativo.

Navegue até a pasta do projeto no seu terminal.

Execute o aplicativo:

python main.py

🔒 Regras de Acesso e Uso
Acesso Normal (Usuário)
Clique em Cadastrar.

Crie um usuário com uma Matrícula (somente números) e Senha (mínimo de 8 caracteres alfanuméricos).

Volte para a tela principal e clique em Entrar.

⚙️ Tecnologias Utilizadas
Interface Gráfica: PyQt6

Lógica de Negócio: Python

Persistência de Dados: SQLite3

Segurança: Bcrypt (Hashing de Senhas)
