# banco.py
# Gerenciamento do banco de dados SQLite para persistência e sincronização de dados.
import sqlite3
# Importa a biblioteca bcrypt para o hashing seguro de senhas.
import bcrypt
# Importa a biblioteca datetime para registrar o horário das reservas.
from datetime import datetime

# Define o nome do arquivo do banco de dados (será criado na mesma pasta do projeto).
DB_NAME = 'reservas_salas.db'

# Função auxiliar para configurar o cursor do SQLite para retornar dicionários (Rows)
def dict_factory(cursor, row):
    d = {}
    # Itera sobre as colunas e seus valores na linha.
    for idx, col in enumerate(cursor.description):
        # Mapeia o nome da coluna (col[0]) ao seu valor.
        d[col[0]] = row[idx]
    return d

# Função para estabelecer a conexão com o SQLite.
def get_db_connection():
    # Conecta ao banco de dados; se o arquivo não existir, ele é criado.
    conn = sqlite3.connect(DB_NAME)
    # Configura a conexão para usar a função dict_factory, retornando dicionários em vez de tuplas.
    conn.row_factory = dict_factory 
    return conn

# Função para inicializar as tabelas (garante que a estrutura do banco exista).
def inicializar_tabelas():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Cria a tabela USUARIOS se ela não existir.
    cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            matricula TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            senha_hash TEXT NOT NULL
        );
    """)
    # Cria a tabela RESERVAS se ela não existir.
    cur.execute("""
        CREATE TABLE IF NOT EXISTS reservas (
            sala TEXT NOT NULL,
            slot_horario TEXT NOT NULL,
            matricula_usuario TEXT NOT NULL,
            nome_usuario TEXT NOT NULL,
            horario_registro TEXT NOT NULL,
            -- Define uma chave composta para garantir que o mesmo slot na mesma sala não possa ser reservado duas vezes.
            PRIMARY KEY (sala, slot_horario)
        );
    """)
    # Salva as alterações (criação das tabelas) no banco.
    conn.commit()
    conn.close()

# Garante que o banco seja criado e inicializado assim que o módulo é importado
inicializar_tabelas() 

# ----------------- FUNÇÕES ADMIN ------------------

def listar_usuarios_com_reservas():
    """Busca todos os usuários e associa suas reservas para exibição na área Admin."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # 1. Busca todos os usuários (incluindo o hash da senha para o admin).
    cur.execute("SELECT matricula, nome, senha_hash FROM usuarios")
    # Cria um dicionário mapeando matrícula a todos os dados do usuário.
    users_data = {row['matricula']: dict(row) for row in cur.fetchall()}
    
    # 2. Busca todas as reservas ativas.
    cur.execute("SELECT matricula_usuario, sala, slot_horario FROM reservas ORDER BY matricula_usuario, slot_horario")
    reservations = cur.fetchall()
    
    # 3. Inicializa uma estrutura para armazenar as reservas por matrícula.
    users_reservations = {matricula: [] for matricula in users_data.keys()}
    
    # Associa cada reserva ao seu respectivo usuário.
    for row in reservations:
        matricula = row['matricula_usuario']
        if matricula in users_reservations:
            # Formata a reserva como string (ex: "Biblioteca (13:00 - 13:50)").
            users_reservations[matricula].append(f"{row['sala']} ({row['slot_horario']})")
    
    # 4. Combina os dados e formata a lista final para a tabela.
    final_list = []
    for matricula, user_info in users_data.items():
        # Concatena todas as reservas em uma única string, separadas por quebra de linha (\n).
        reservas_str = "\n".join(users_reservations.get(matricula, ["Nenhuma reserva ativa"]))
        
        # Adiciona a string de reservas ao dicionário do usuário.
        user_info['reservas_ativas'] = reservas_str
        final_list.append(user_info)
        
    conn.close()
    return final_list

# ----------------- FUNÇÕES DE AUTENTICAÇÃO E RESERVA ------------------

def cadastrar_usuario(matricula, nome, senha):
    """Insere um novo usuário no banco com a senha criptografada."""
    conn = get_db_connection()
    cur = conn.cursor()
    # Gera o hash da senha usando Bcrypt (criptografia).
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    try:
        cur.execute(
            "INSERT INTO usuarios (matricula, nome, senha_hash) VALUES (?, ?, ?)",
            (matricula, nome, senha_hash)
        )
        conn.commit()
        return True, "Usuário cadastrado com sucesso!"
    # Captura erro de chave primária duplicada (matrícula já existe).
    except sqlite3.IntegrityError:
        return False, "Matrícula já existe."
    finally:
        conn.close()

def verificar_login(matricula, senha):
    """Verifica as credenciais do usuário usando o hash da senha."""
    conn = get_db_connection()
    cur = conn.cursor()
    # Busca o usuário pela matrícula.
    cur.execute("SELECT matricula, nome, senha_hash FROM usuarios WHERE matricula = ?", (matricula,))
    usuario = cur.fetchone()

    # Se o usuário for encontrado e o hash da senha for compatível (Bcrypt.checkpw)...
    if usuario and bcrypt.checkpw(senha.encode('utf-8'), usuario['senha_hash'].encode('utf-8')):
        # Retorna o dicionário com os dados do usuário.
        return dict(usuario)
    # Caso contrário, retorna None.
    return None

def carregar_reservas_do_banco():
    """Busca todas as reservas ativas no banco para sincronização."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT sala, slot_horario, nome_usuario, matricula_usuario, horario_registro FROM reservas")
    reservas_db = {}
    for row in cur.fetchall():
        sala = row['sala']
        slot_horario = row['slot_horario']
        if sala not in reservas_db: reservas_db[sala] = {}
        # Armazena as informações da reserva no dicionário.
        reservas_db[sala][slot_horario] = {
            'nome': row['nome_usuario'],
            'matricula': row['matricula_usuario'],
            'horario_slot': slot_horario,
            'horario_registro': row['horario_registro']
        }
    conn.close()
    return reservas_db

def salvar_reserva_no_banco(sala, slot_horario, nome_usuario, matricula_usuario, horario_registro):
    """Salva uma nova reserva no banco de dados."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # Usa INSERT OR REPLACE para evitar erros se a chave primária já existir (embora a lógica do PyQt já previna isso).
        cur.execute("""
            INSERT OR REPLACE INTO reservas (sala, slot_horario, nome_usuario, matricula_usuario, horario_registro)
            VALUES (?, ?, ?, ?, ?)
        """, (sala, slot_horario, nome_usuario, matricula_usuario, horario_registro))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao salvar reserva: {e}")
        return False
    finally:
        conn.close()

def deletar_reserva_do_banco(sala, slot_horario):
    """Remove uma reserva específica do banco."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM reservas WHERE sala = ? AND slot_horario = ?", (sala, slot_horario))
        conn.commit()
        # Retorna True se pelo menos uma linha foi afetada.
        return cur.rowcount > 0
    except Exception as e:
        print(f"Erro ao deletar reserva: {e}")
        return False
    finally:
        conn.close()

def deletar_usuario(matricula):
    """Remove um usuário e todas as suas reservas em uma única transação."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # 1. Exclui todas as reservas ligadas à matrícula.
        cur.execute("DELETE FROM reservas WHERE matricula_usuario = ?", (matricula,))
        # 2. Exclui o usuário da tabela principal.
        cur.execute("DELETE FROM usuarios WHERE matricula = ?", (matricula,))
        conn.commit()
        return True, f"Usuário {matricula} e suas reservas excluídos."
    except Exception as e:
        print(f"Erro ao deletar usuário: {e}")
        # Desfaz todas as operações se houver um erro.
        conn.rollback()
        return False, "Erro ao excluir usuário e reservas."
    finally:
        conn.close()
