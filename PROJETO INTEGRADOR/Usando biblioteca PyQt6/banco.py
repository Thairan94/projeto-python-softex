# banco.py
import sqlite3
from datetime import datetime

# Define o nome do arquivo do banco de dados
DB_NAME = 'reservas_salas.db'

# Função auxiliar para configurar o cursor para retornar dicionários (Rows)
def dict_factory(cursor, row):
    # Cria um dicionário a partir dos resultados da consulta, usando os nomes das colunas como chaves.
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def conectar_db():
    """Estabelece a conexão com o banco de dados."""
    conn = sqlite3.connect(DB_NAME)
    # Define a função que o cursor usará para formatar os resultados.
    conn.row_factory = dict_factory
    return conn

def inicializar_banco():
    """Cria as tabelas USUARIOS e RESERVAS se elas ainda não existirem."""
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Tabela de Usuários (para a lógica de login/cadastro)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            matricula TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            senha TEXT NOT NULL
        );
    """)
    
    # Tabela de Reservas (compartilhada entre todos os usuários)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservas (
            sala TEXT NOT NULL,
            slot_horario TEXT NOT NULL,
            nome_usuario TEXT NOT NULL,
            matricula_usuario TEXT NOT NULL,
            horario_registro TEXT NOT NULL,
            -- Define uma chave composta para garantir que o mesmo slot na mesma sala não possa ser reservado duas vezes.
            PRIMARY KEY (sala, slot_horario)
        );
    """)
    conn.commit()
    conn.close()

# --- Funções CRUD de Usuários ---

def cadastrar_usuario(matricula, nome, senha):
    """Insere um novo usuário no banco de dados, verificando se a matrícula já existe."""
    conn = conectar_db()
    cursor = conn.cursor()
    
    # 1. Verifica se a matrícula já existe.
    cursor.execute("SELECT matricula FROM usuarios WHERE matricula = ?", (matricula,))
    if cursor.fetchone():
        conn.close()
        return False, "Erro: Matrícula já cadastrada."
        
    # 2. Insere o novo usuário.
    try:
        cursor.execute("INSERT INTO usuarios (matricula, nome, senha) VALUES (?, ?, ?)", 
                       (matricula, nome, senha))
        conn.commit()
        return True, "Usuário cadastrado com sucesso!"
    except Exception:
        return False, "Erro ao salvar o usuário no banco de dados."
    finally:
        conn.close()

def verificar_login(matricula, senha):
    """Verifica as credenciais do usuário."""
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT nome, matricula FROM usuarios WHERE matricula = ? AND senha = ?", (matricula, senha))
    usuario = cursor.fetchone()
    conn.close()
    
    # Retorna o dicionário do usuário se encontrado, caso contrário, retorna None.
    return usuario

def listar_usuarios():
    """Lista todos os usuários cadastrados (para a tela Admin)."""
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, matricula, senha FROM usuarios ORDER BY nome")
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

def deletar_usuario(matricula):
    """Deleta um usuário e todas as suas reservas (para a tela Admin)."""
    conn = conectar_db()
    cursor = conn.cursor()
    
    try:
        # 1. Deleta todas as reservas associadas à matrícula.
        cursor.execute("DELETE FROM reservas WHERE matricula_usuario = ?", (matricula,))
        
        # 2. Deleta o usuário.
        cursor.execute("DELETE FROM usuarios WHERE matricula = ?", (matricula,))
        conn.commit()
        return True, "Usuário e suas reservas excluídos com sucesso!"
    except Exception as e:
        print(f"Erro ao deletar usuário: {e}")
        return False, "Erro ao excluir usuário e reservas."
    finally:
        conn.close()


# --- Funções CRUD de Reservas (Mantidas) ---

def carregar_reservas_do_banco():
    """Carrega todas as reservas ativas do banco de dados para a memória."""
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Adicionamos 'matricula_usuario' aqui para a lógica de exclusão no Admin.
    cursor.execute("SELECT sala, slot_horario, nome_usuario, matricula_usuario, horario_registro FROM reservas")
    
    reservas_db = {}
    
    for reserva in cursor.fetchall():
        sala = reserva['sala']
        slot_horario = reserva['slot_horario']
        
        if sala not in reservas_db:
            reservas_db[sala] = {}
            
        reservas_db[sala][slot_horario] = {
            'nome': reserva['nome_usuario'],
            'matricula': reserva['matricula_usuario'],
            'horario_slot': slot_horario,
            'horario_registro': reserva['horario_registro']
        }
        
    conn.close()
    return reservas_db

def salvar_reserva_no_banco(sala, slot_horario, nome_usuario, matricula_usuario, horario_registro):
    """Insere um novo registro de reserva no banco de dados."""
    conn = conectar_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT OR REPLACE INTO reservas (sala, slot_horario, nome_usuario, matricula_usuario, horario_registro)
            VALUES (?, ?, ?, ?, ?)
        """, (sala, slot_horario, nome_usuario, matricula_usuario, horario_registro))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()

def deletar_reserva_do_banco(sala, slot_horario):
    """Remove um registro de reserva do banco de dados (cancelamento)."""
    conn = conectar_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            DELETE FROM reservas
            WHERE sala = ? AND slot_horario = ?
        """, (sala, slot_horario))
        conn.commit()
        return cursor.rowcount > 0 
    except Exception:
        return False
    finally:
        conn.close()

# Chamada inicial para garantir que o banco está pronto
inicializar_banco()
