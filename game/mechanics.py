# game/mechanics.py
# Implementa a lógica do recurso compartilhado (Mesa) e o controle com semáforo.

import threading
import time
import random
import pygame
from queue import Queue
from ..settings import VAGAS_NA_MESA

class GerenciadorMesa:
    """
    Gerencia o acesso à mesa de presentes usando semáforos.
    Simula o problema produtor-consumidor clássico de SO.
    """
    
    def __init__(self, capacidade=VAGAS_NA_MESA):
        self.capacidade = capacidade
        self.semaforo = threading.Semaphore(capacidade)  # Controla acesso à mesa
        self.mutex = threading.Lock()  # Protege operações críticas
        self.presentes = []  # Lista de presentes na mesa
        self.total_presentes_processados = 0
        
    def adicionar_presente(self, presente):
        """
        Adiciona um presente à mesa (seção crítica protegida por semáforo).
        Retorna True se conseguiu adicionar, False se mesa cheia.
        """
        # Tenta adquirir uma vaga na mesa (não-bloqueante)
        if self.semaforo.acquire(blocking=False):
            try:
                with self.mutex:  # Seção crítica
                    if len(self.presentes) < self.capacidade:
                        self.presentes.append(presente)
                        print(f"[MESA] Presente adicionado. Total: {len(self.presentes)}/{self.capacidade}")
                        return True
                    else:
                        # Caso improvável, mas por segurança
                        self.semaforo.release()
                        return False
            except Exception as e:
                self.semaforo.release()  # Libera em caso de erro
                print(f"[ERRO] Ao adicionar presente: {e}")
                return False
        else:
            print("[MESA] Mesa cheia! Não foi possível adicionar presente.")
            return False
    
    def remover_presente(self):
        """
        Remove um presente da mesa (elfo coletando).
        Retorna o presente removido ou None se mesa vazia.
        """
        with self.mutex:  # Seção crítica
            if self.presentes:
                presente = self.presentes.pop(0)  # FIFO
                self.total_presentes_processados += 1
                self.semaforo.release()  # Libera uma vaga
                print(f"[MESA] Presente coletado! Restam: {len(self.presentes)}/{self.capacidade}")
                return presente
            else:
                print("[MESA] Mesa vazia! Nada para coletar.")
                return None
    
    def esta_cheia(self):
        """Verifica se a mesa está cheia."""
        with self.mutex:
            return len(self.presentes) >= self.capacidade
    
    def esta_vazia(self):
        """Verifica se a mesa está vazia."""
        with self.mutex:
            return len(self.presentes) == 0
    
    def get_status(self):
        """Retorna status atual da mesa."""
        with self.mutex:
            return {
                'presentes_na_mesa': len(self.presentes),
                'capacidade': self.capacidade,
                'total_processados': self.total_presentes_processados,
                'ocupacao_percentual': (len(self.presentes) / self.capacidade) * 100
            }

class ProdutorPresentes(threading.Thread):
    """
    Thread produtora que gera presentes continuamente.
    Simula um processo produtor no problema produtor-consumidor.
    """
    
    def __init__(self, esteira_id, gerenciador_mesa, fila_presentes_visuais, intervalo_inicial=3.0):
        super().__init__()
        self.esteira_id = esteira_id
        self.gerenciador_mesa = gerenciador_mesa
        self.fila_presentes_visuais = fila_presentes_visuais  # Fila para comunicar com o jogo
        self.intervalo_producao = intervalo_inicial
        self.running = True
        self.daemon = True  # Thread termina quando programa principal termina
        self.presentes_criados = 0
        
    def run(self):
        """Loop principal da thread produtora."""
        while self.running:
            try:
                # Simula tempo de produção
                time.sleep(self.intervalo_producao)
                
                if self.running:  # Verifica novamente após sleep
                    self.produzir_presente()
                    
            except Exception as e:
                print(f"[ERRO] Thread produtora {self.esteira_id}: {e}")
                break
    
    def produzir_presente(self):
        """Cria um novo presente e tenta adicioná-lo ao sistema."""
        presente_data = {
            'id': f"presente_{self.esteira_id}_{self.presentes_criados}",
            'esteira_origem': self.esteira_id,
            'timestamp': time.time(),
            'tipo': random.choice(['presente_visual_1', 'presente_visual_2', 'presente_visual_3', 'presente_visual_4'])
        }
        
        self.presentes_criados += 1
        
        # Coloca o presente na fila para o jogo processar visualmente
        try:
            self.fila_presentes_visuais.put(presente_data, block=False)
            print(f"[PRODUTOR {self.esteira_id}] Presente #{self.presentes_criados} criado")
        except:
            print(f"[PRODUTOR {self.esteira_id}] Fila de presentes cheia!")
    
    def acelerar_producao(self, fator=0.9):
        """Acelera a produção (diminui intervalo)."""
        self.intervalo_producao = max(0.5, self.intervalo_producao * fator)
        print(f"[PRODUTOR {self.esteira_id}] Produção acelerada para {self.intervalo_producao:.2f}s")
    
    def parar(self):
        """Para a thread produtora."""
        self.running = False

class EscalonadorJogo:
    """
    Simula um escalonador de SO, controlando a dificuldade do jogo
    e o balanceamento entre produtores.
    """
    
    def __init__(self, produtores, intervalo_escalonamento=10.0):
        self.produtores = produtores
        self.intervalo_escalonamento = intervalo_escalonamento
        self.running = True
        self.nivel_dificuldade = 1
        self.thread_escalonador = threading.Thread(target=self._loop_escalonamento)
        self.thread_escalonador.daemon = True
        
    def iniciar(self):
        """Inicia o escalonador."""
        self.thread_escalonador.start()
        print("[ESCALONADOR] Iniciado!")
        
    def _loop_escalonamento(self):
        """Loop principal do escalonador."""
        while self.running:
            try:
                time.sleep(self.intervalo_escalonamento)
                if self.running:
                    self._ajustar_dificuldade()
            except Exception as e:
                print(f"[ERRO] Escalonador: {e}")
                break
    
    def _ajustar_dificuldade(self):
        """Ajusta a dificuldade do jogo aumentando velocidade de produção."""
        self.nivel_dificuldade += 1
        
        # Acelera todos os produtores
        for produtor in self.produtores:
            if produtor.is_alive():
                produtor.acelerar_producao(0.85)  # Cada nível fica 15% mais rápido
        
        print(f"[ESCALONADOR] Nível {self.nivel_dificuldade} - Dificuldade aumentada!")
    
    def parar(self):
        """Para o escalonador."""
        self.running = False

class GameMechanics:
    """
    Classe principal que integra todas as mecânicas de SO no jogo.
    """
    
    def __init__(self):
        self.gerenciador_mesa = GerenciadorMesa()
        self.fila_presentes_visuais = Queue(maxsize=50)  # Comunicação thread-safe com jogo
        
        # Criação dos produtores (uma thread por esteira)
        self.produtores = [
            ProdutorPresentes(1, self.gerenciador_mesa, self.fila_presentes_visuais, 4.0),
            ProdutorPresentes(2, self.gerenciador_mesa, self.fila_presentes_visuais, 3.5),
            ProdutorPresentes(3, self.gerenciador_mesa, self.fila_presentes_visuais, 3.0)
        ]
        
        # Escalonador para aumentar dificuldade
        self.escalonador = EscalonadorJogo(self.produtores)
        
        self.pontuacao = 0
        self.presentes_perdidos = 0
        self.iniciado = False
        
    def iniciar_sistema(self):
        """Inicia todas as threads e o sistema de mecânicas."""
        if not self.iniciado:
            print("[SISTEMA] Iniciando mecânicas de SO...")
            
            # Inicia threads produtoras
            for produtor in self.produtores:
                produtor.start()
            
            # Inicia escalonador
            self.escalonador.iniciar()
            
            self.iniciado = True
            print("[SISTEMA] Todas as mecânicas iniciadas!")
    
    def parar_sistema(self):
        """Para todas as threads do sistema."""
        if self.iniciado:
            print("[SISTEMA] Parando mecânicas...")
            
            # Para produtores
            for produtor in self.produtores:
                produtor.parar()
            
            # Para escalonador
            self.escalonador.parar()
            
            self.iniciado = False
            print("[SISTEMA] Sistema parado!")
    
    def processar_novos_presentes(self):
        """
        Processa presentes criados pelas threads produtoras.
        Deve ser chamado no loop principal do jogo.
        """
        presentes_processados = []
        
        # Processa todos os presentes na fila
        while not self.fila_presentes_visuais.empty():
            try:
                presente_data = self.fila_presentes_visuais.get_nowait()
                presentes_processados.append(presente_data)
            except:
                break
        
        return presentes_processados
    
    def elfo_tentar_coletar(self):
        """
        Simula elfo tentando coletar presente da mesa.
        Retorna True se coletou, False se mesa vazia.
        """
        presente = self.gerenciador_mesa.remover_presente()
        if presente:
            self.pontuacao += 10
            return True
        return False
    
    def adicionar_presente_mesa(self, presente_data):
        """
        Adiciona presente à mesa (quando elfo entrega).
        Retorna True se conseguiu, False se mesa cheia.
        """
        sucesso = self.gerenciador_mesa.adicionar_presente(presente_data)
        if not sucesso:
            self.presentes_perdidos += 1
            print("[PENALIDADE] Presente perdido! Mesa cheia.")
        return sucesso
    
    def get_estatisticas(self):
        """Retorna estatísticas do jogo."""
        mesa_status = self.gerenciador_mesa.get_status()
        return {
            'pontuacao': self.pontuacao,
            'presentes_perdidos': self.presentes_perdidos,
            'nivel_dificuldade': self.escalonador.nivel_dificuldade,
            'mesa_status': mesa_status,
            'produtores_ativos': sum(1 for p in self.produtores if p.is_alive())
        }