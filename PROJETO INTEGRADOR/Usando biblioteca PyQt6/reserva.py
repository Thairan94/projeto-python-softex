# reserva.py

# Importa classes do PyQt6 para criar a interface.
# QWidget (janela), QVBoxLayout (layout vertical), QPushButton (botão), QLabel (rótulo).
# QMessageBox (caixa de diálogo de mensagem), QInputDialog (diálogo para entrada/seleção).
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QInputDialog
# Importa a classe Qt para acessar constantes (como alinhamento).
from PyQt6.QtCore import Qt
# Importa QCursor para mudar o cursor do mouse.
from PyQt6.QtGui import QCursor
# Importa a biblioteca datetime e timedelta para trabalhar com datas e cálculos de tempo.
from datetime import datetime, timedelta
# Importa as funções de banco de dados para sincronização multiusuário
from banco import carregar_reservas_do_banco, salvar_reserva_no_banco, deletar_reserva_do_banco

# Define a classe AppReservaSalas, que é a janela principal de reservas.
class AppReservaSalas(QWidget):
    # Construtor da classe. Recebe a janela anterior (Login), nome e matrícula do usuário.
    def __init__(self, janela_anterior, nome_usuario, matricula_usuario):
        # Chama o construtor da classe base (QWidget).
        super().__init__()
        # Armazena a janela anterior para navegação.
        self.janela_anterior = janela_anterior
        # Armazena o nome do usuário logado.
        self.nome_usuario = nome_usuario
        # Armazena a matrícula do usuário logado (usada para limite/cancelamento).
        self.matricula_usuario = matricula_usuario 
        # Define o título e as dimensões da janela.
        self.setWindowTitle("Sistema de Reserva de Salas")
        self.setGeometry(100, 100, 450, 400)
        # Define o estilo CSS base para a janela.
        self.setStyleSheet("QWidget { background-color: #f0f0f0; font-family: Arial; }")

        # Define os slots de horários fixos (50 minutos de duração).
        self.horarios_slots = self._gerar_slots_horarios()

        # Dicionário principal para armazenar o estado das salas E slots.
        # Inicializa cada sala com todos os slots como None (disponível).
        self.salas = {
            "Biblioteca": {slot: None for slot in self.horarios_slots},
            "Sala 01": {slot: None for slot in self.horarios_slots},
            "Sala 02": {slot: None for slot in self.horarios_slots},
            "Informática": {slot: None for slot in self.horarios_slots},
            "Robótica": {slot: None for slot in self.horarios_slots},
            "Ciências": {slot: None for slot in self.horarios_slots},
        }
        
        # Chama a função para carregar dados persistentes do banco e mesclar com os slots vazios
        self._carregar_e_mesclar_reservas()
        
        # Dicionário para armazenar as referências aos objetos QPushButton (botões de sala).
        self.botoes = {}
        # Chama os métodos para inicializar a interface e o estado.
        self.criar_interface()
        self.atualizar_interface()

    # Método interno para calcular e gerar os slots de horário.
    def _gerar_slots_horarios(self):
        """Gera os slots de horário fixos (50 minutos)."""
        slots = []
        # Define a hora de início (13:00).
        hora_inicio = datetime.strptime("13:00", "%H:%M")
        num_slots = 5 
        duracao_minutos = 50

        # Loop para criar 5 slots.
        for _ in range(num_slots):
            # Calcula o horário de término.
            hora_fim = hora_inicio + timedelta(minutes=duracao_minutos)
            # Formata o slot como string (ex: "13:00 - 13:50").
            slot_str = f"{hora_inicio.strftime('%H:%M')} - {hora_fim.strftime('%H:%M')}"
            slots.append(slot_str)
            # A nova hora de início é a hora de término anterior.
            hora_inicio = hora_fim
        return slots

    # Método interno para buscar dados do SQLite e atualizar o dicionário self.salas.
    def _carregar_e_mesclar_reservas(self):
        """Carrega dados do banco e mescla com a estrutura de slots."""
        # Chama a função do banco para buscar todas as reservas persistentes.
        reservas_db = carregar_reservas_do_banco()
        
        # Itera sobre as salas e seus slots ocupados retornados pelo banco.
        for sala_nome, slots_ocupados in reservas_db.items():
            # Verifica se a sala do banco existe no nosso dicionário de salas.
            if sala_nome in self.salas:
                # Itera sobre os slots que estão ocupados no banco.
                for slot, info_reserva in slots_ocupados.items():
                    # Garante que o slot de horário é válido.
                    if slot in self.horarios_slots:
                        # Atualiza o slot no dicionário self.salas com as informações da reserva.
                        self.salas[sala_nome][slot] = info_reserva

    # Método que constrói os elementos visuais da tela.
    def criar_interface(self):
        """Método que constrói os elementos visuais da tela."""
        # Cria o layout vertical principal.
        layout_principal = QVBoxLayout()
        # Define o espaçamento entre os widgets.
        layout_principal.setSpacing(10)
        # Aplica o layout à janela.
        self.setLayout(layout_principal)

        # Rótulo de boas-vindas.
        titulo = QLabel(f"Bem-vindo(a), {self.nome_usuario}!")
        titulo.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(titulo)

        # Subtítulo informativo sobre a regra de limite de reservas.
        subtitulo = QLabel("Máx. 2 reservas por usuário. Clique em uma sala para ver os horários.")
        subtitulo.setStyleSheet("font-size: 12px; color: #666;")
        subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(subtitulo)

        # Cria os botões para cada sala.
        for sala in self.salas:
            botao = QPushButton(f"Ver Horários: {sala}")
            botao.setFixedHeight(50)
            # Estilo CSS para os botões.
            botao.setStyleSheet("""
                QPushButton { background-color: #333; color: white; border-radius: 8px; font-size: 18px; }
                QPushButton:hover { background-color: #555; }
            """)
            botao.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            # Conecta o clique do botão para abrir o diálogo de slots.
            botao.clicked.connect(lambda _, s=sala: self.mostrar_slots_sala(s))
            self.botoes[sala] = botao
            layout_principal.addWidget(botao)

    # Método para exibir a janela de seleção de slots de horário.
    def mostrar_slots_sala(self, sala):
        """Método para exibir a janela de seleção de slots de horário para uma sala."""
        # Cria o diálogo de entrada (QInputDialog).
        dialogo = QInputDialog(self)
        dialogo.setWindowTitle(f"Horários para {sala}")
        dialogo.setLabelText("Escolha um horário:")
        
        slots_com_status = []
        status_sala = self.salas[sala]
        
        # Preenche a lista do diálogo com o status de cada slot.
        for slot in self.horarios_slots:
            if status_sala[slot] is None:
                # Slot disponível (texto (Disponível) incluído).
                slots_com_status.append(f"{slot} (Disponível)") 
            else:
                # Slot ocupado.
                reservado_por = status_sala[slot]['nome']
                if status_sala[slot]['matricula'] == self.matricula_usuario:
                    # Slot reservado pelo próprio usuário.
                    slots_com_status.append(f"{slot} (MINHA RESERVA)")
                else:
                    # Slot ocupado por outro usuário.
                    slots_com_status.append(f"{slot} (Ocupado por {reservado_por})") 
        
        # Define os itens da lista suspensa do diálogo.
        dialogo.setComboBoxItems(slots_com_status)
        
        # Executa o diálogo e espera pela interação do usuário.
        ok = dialogo.exec()
        
        # Se o usuário clicou em OK...
        if ok:
            slot_escolhido_completo = dialogo.textValue()
            # Extrai apenas a string do horário, removendo o status entre parênteses.
            slot_escolhido = slot_escolhido_completo.split(" (")[0]
            
            # Chama a função principal de reserva/cancelamento.
            self.reservar_sala(sala, slot_escolhido)

    # Método que atualiza a cor dos botões conforme o estado das reservas.
    def atualizar_interface(self):
        """Método que atualiza o texto e a cor dos botões conforme o estado das reservas."""
        for sala in self.salas:
            botao = self.botoes[sala]
            
            # Checa se o usuário logado tem pelo menos um slot reservado nesta sala.
            reservado_por_mim_em_algum_slot = False
            for status in self.salas[sala].values():
                # Usa a matrícula para checagem (mais seguro).
                if status is not None and status['matricula'] == self.matricula_usuario:
                    reservado_por_mim_em_algum_slot = True
                    break

            # Aplica o estilo amarelo se o usuário tiver reservado algo.
            if reservado_por_mim_em_algum_slot:
                botao.setStyleSheet("""
                    QPushButton { background-color: #FFC107; color: #333; border-radius: 8px; font-size: 18px; }
                    QPushButton:hover { background-color: #FFB300; }
                """)
            else:
                # Aplica o estilo padrão (cinza/preto).
                 botao.setStyleSheet("""
                    QPushButton { background-color: #333; color: white; border-radius: 8px; font-size: 18px; }
                    QPushButton:hover { background-color: #555; }
                """)
            
            botao.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    # Método principal para lidar com a reserva e o cancelamento.
    def reservar_sala(self, sala, slot):
        """Método principal para lidar com a reserva e o cancelamento."""
        info_reserva = self.salas[sala][slot]
        
        # 1. Lógica de Cancelamento: Se o slot está reservado pelo usuário logado...
        if info_reserva is not None and info_reserva['matricula'] == self.matricula_usuario:
            # Pede confirmação.
            resposta = QMessageBox.question(self, "Confirmação de Cancelamento",
                                            f"Deseja realmente cancelar sua reserva da sala {sala} no horário {slot}?",
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            
            if resposta == QMessageBox.StandardButton.Yes:
                # Chama a função do banco para deletar o registro.
                if deletar_reserva_do_banco(sala, slot):
                    # Limpa o slot na memória.
                    self.salas[sala][slot] = None
                    QMessageBox.information(self, "Cancelamento", f"Reserva da sala {sala} no horário {slot} cancelada com sucesso.")
                    # Recarrega e atualiza a interface.
                    self._carregar_e_mesclar_reservas() 
                    self.atualizar_interface()
                else:
                    QMessageBox.critical(self, "Erro", "Não foi possível cancelar a reserva no banco de dados.")
            return

        # 2. Lógica de Tentativa de Reserva
        if info_reserva is not None:
            # Slot ocupado por outro usuário.
            mensagem = (f"O horário {slot} na sala {sala} já está reservado!\n\n"
                        f"Reservado por: {info_reserva['nome']}\n"
                        f"Horário da Reserva: {info_reserva['horario_registro']}")
            QMessageBox.warning(self, "Horário Indisponível", mensagem)
        
        else:
            # 2.1 Verifica a regra de limite de 2 reservas
            reservas_count = 0
            # Conta o número total de reservas ativas deste usuário.
            for sala_slots in self.salas.values():
                for status in sala_slots.values():
                    if status is not None and status['matricula'] == self.matricula_usuario:
                        reservas_count += 1
            
            if reservas_count >= 2:
                QMessageBox.warning(self, "Limite Excedido", "Você já tem o máximo de 2 salas/horários reservados. Cancele um para reservar outro.")
                return

            # 2.2 Faz a nova reserva
            horario_registro = datetime.now().strftime("%H:%M:%S em %d/%m/%Y")
            
            # Chama a função do banco para salvar a nova reserva.
            if salvar_reserva_no_banco(sala, slot, self.nome_usuario, self.matricula_usuario, horario_registro):
                
                # Após salvar, recarrega os dados do banco e atualiza a interface.
                self._carregar_e_mesclar_reservas()
                
                QMessageBox.information(self, "Sucesso!", f"Slot {slot} na sala {sala} reservado por {self.nome_usuario}!")
                self.atualizar_interface()
            else:
                QMessageBox.critical(self, "Erro", "Não foi possível salvar a reserva. Tente novamente.")
