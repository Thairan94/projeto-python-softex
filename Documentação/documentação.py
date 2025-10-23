# 🚀 Como Rodar o Projeto Siga os passos abaixo para configurar e executar o aplicativo em sua máquina.

# Pré-requisitos Você precisa ter o Python 3 instalado em seu sistema.

# Instalação das Dependências Abra seu terminal ou prompt de comando (PowerShell/CMD) e instale as bibliotecas necessárias: PyQt6 e Bcrypt.

# pip install PyQt6 bcrypt

# Estrutura do Projeto Certifique-se de que todos os arquivos (main.py, login.py, banco.py, etc.) estão localizados na mesma pasta:
# /SeuProjeto/ ├── main.py ├── login.py ├── cadastro.py ├── reserva.py ├── admin.py ├── banco.py <- Módulo de acesso ao Banco de Dados └── reservas_salas.db <- Arquivo do banco de dados (criado automaticamente)

# Inicialização do Sistema O arquivo main.py é o ponto de entrada do aplicativo.
# Navegue até a pasta do projeto no seu terminal.

# Execute o aplicativo:

# python main.py

# 🔒 Regras de Negócio e Segurança
# As seguintes regras de segurança e negócio foram implementadas:

# 1. Autenticação e Sincronização
# Login Centralizado: O sistema exige matrícula e senha válidas. A matrícula é o identificador único e é validada diretamente no banco de dados (SQLite).

# Segurança no Cadastro: A Matrícula aceita somente números, e a Senha deve ser alfanumérica e ter no mínimo 8 caracteres.

# Sincronização: As reservas são salvas no banco de dados. Quando qualquer usuário faz uma reserva, o estado da sala é atualizado no banco, e todos os outros usuários verão a mudança na próxima consulta.

# 2. Regras de Reserva
# Limite de Uso: Cada usuário pode reservar no máximo dois (2) slots de horário. Ao tentar a terceira reserva, o sistema emite um alerta de limite excedido.

# Cancelamento: O usuário só pode cancelar uma reserva que ele mesmo efetuou.

# Slots Fixos: As salas são reservadas em blocos de 50 minutos (ex.: 13:00 - 13:50).

# 3. Gerenciamento (Área Admin)
# Acesso Restrito: Existe um login especial (admin / 12345678) que dá acesso a uma área de gerenciamento.

# Controle de Usuários: O administrador pode visualizar todos os usuários cadastrados (Nome, Matrícula, Senha) e tem a funcionalidade de Excluir qualquer usuário e suas reservas associadas.

# Roteiro Sugerido para Demonstração
# Use este roteiro para uma apresentação rápida e impactante:

# Início: Rode main.py. Mostre a tela de Login.

# Fluxo de Cadastro: Clique em "Cadastrar". Demonstre a regra de validação de matrícula (somente números) e a senha (mínimo de 8 caracteres).

# Login de Usuário (João): Faça login com um usuário recém-cadastrado (ex.: "João").

# Teste de Regra (Limite):

# João reserva a Sala A no Slot 1.

# João reserva a Sala B no Slot 2.

# João tenta reservar a Sala C. Mostre a mensagem de "Limite Excedido".

# Teste Multiusuário (Maria):

# Saia do programa e entre novamente (simulando outro computador) ou peça para um colega abrir o programa em outra máquina.

# Faça login com outro usuário (ex.: "Maria").

# Maria tenta reservar a Sala A no Slot 1. Mostre o aviso: "Ocupado por João".

# Gerenciamento:

# Saia do programa e entre com o login Admin (admin / 12345678).

# Mostre a tabela de usuários e exclua o usuário Maria.

# Mencione que a exclusão do usuário também deleta todas as reservas dele do banco.