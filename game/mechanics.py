#   game/mechanics.py
"""
Arquivo que contém as mecânicas principais do jogo, integrando
threads, semáforos e filas para simular o gerenciamento de presentes.
Essa mecânica foi desenvolvida com o intuito de ilustrar de forma didática
conceitos clássicos de sistemas operacionais, envolvendo threads
e semáforos.
Conceitos envolvidos: Threads (Produtor-Consumidor), Semáforos (Recurso Compartilhado),
Mutex (Seção Crítica) e Escalonador (Dificuldade Dinâmica).
"""
import threading    # Importa o módulo threading para manipulação de threads
import time # Importa o módulo time para manipulação de tempo
import random   # Importa o módulo random para geração de números aleatórios
import pygame   # Importa o módulo pygame para manipulação de gráficos e áudio
from queue import Queue # Importa a classe Queue para filas thread-safe
from ..settings import VAGAS_NA_MESA    # Importa a constante VAGAS_NA_MESA do arquivo de configurações


class GerenciadorMesa:
    """
    Representa o recurso compartilhado (a mesa) e gerencia o acesso concorrente
    a ela usando semáforos e mutex, simulando o buffer no problema
    Produtor-Consumidor.
    """
    
    def __init__(self, capacidade=VAGAS_NA_MESA):
        self.capacidade = capacidade
        # CONCEITO SO: Semáforo para controlar o número de vagas disponíveis na mesa.
        # Impede que o Elfo adicione presentes se a mesa já estiver cheia.
        # Isso ilustra o conceito de semáforos (um semáforo em sistemas
        # operacionais é um contador que controla o acesso a um recurso compartilhado
        # para evitar condições de corrida - isto é, quando múltiplas threads
        # tentam acessar o mesmo recurso ao mesmo tempo).
        self.semaforo = threading.Semaphore(capacidade)  # Controla acesso à mesa
        # CONCEITO SO: Mutex para proteger a seção crítica onde os presentes são
        # adicionados ou removidos da mesa. Garante que apenas uma thread
        # possa modificar a lista de presentes ao mesmo tempo, evitando
        # condições de corrida.
        # Mutex é um tipo de bloqueio que permite que apenas uma thread
        # acesse um recurso compartilhado por vez. É usado para proteger
        # seções críticas do código, onde múltiplas threads podem tentar
        # modificar o mesmo recurso simultaneamente, o que poderia levar a
        # inconsistências ou erros.
        self.mutex = threading.Lock()  # Protege operações críticas
        self.presentes = []  # Lista de presentes na mesa
        self.total_presentes_processados = 0    # Contador de presentes processados
        
    def adicionar_presente(self, presente):
        """
        Método para adicionar um presente à mesa (elfo entregando).
        Retorna True se conseguiu adicionar, False se mesa cheia.
        Se a mesa estiver cheia, o elfo não pode adicionar mais presentes
        até que um presente seja removido ("coletado por outro elfo"). Simulando
        o problema clássico do Produtor-Consumidor.
        """
        # Tenta adquirir o semáforo sem bloquear, isto é, se não houver vagas
        # disponíveis, retorna False imediatamente.
        if self.semaforo.acquire(blocking=False):   # Se houver vagas
            try:    
                with self.mutex:  # Seção crítica protegida pelo mutex
                    if len(self.presentes) < self.capacidade: # Verifica se ainda há espaço 
                        self.presentes.append(presente) # Adiciona o presente à mesa
                        print(f"[MESA] Presente adicionado. Total: {len(self.presentes)}/{self.capacidade}")
                        return True # Retorna True se conseguiu adicionar
                    else:
                        # Se a mesa já estiver cheia, libera o semáforo, isto é, 
                        # devolve a vaga que foi adquirida.
                        self.semaforo.release() 
                        return False    # Mesa cheia, não conseguiu adicionar
            except Exception as e:  # Em caso de erro ao adicionar o presente
                # Libera o semáforo para evitar deadlock
                self.semaforo.release()  # Libera em caso de erro
                print(f"[ERRO] Ao adicionar presente: {e}")
                return False    # Retorna False se houve erro
        else:
            print("[MESA] Mesa cheia! Não foi possível adicionar presente.")
            return False    # Mesa cheia, não conseguiu adicionar
    
    def remover_presente(self):
        """
        Remove um presente da mesa (elfo coletando).
        Retorna o presente removido ou None se mesa vazia.
        """
        with self.mutex:  # Seção crítica
            if self.presentes:  # Verifica se há presentes na mesa
                presente = self.presentes.pop(0)  # Remove o primeiro presente da lista
                self.total_presentes_processados += 1   # Incrementa o contador de presentes processados
                self.semaforo.release()  # Libera uma vaga
                print(f"[MESA] Presente coletado! Restam: {len(self.presentes)}/{self.capacidade}")
                return presente # Retorna o presente coletado
            else:
                print("[MESA] Mesa vazia! Nada para coletar.")
                return None # Retorna None se não havia presentes
    
    def esta_cheia(self):   
        """Verifica se a mesa está cheia."""
        with self.mutex:    # Protege a seção crítica
            return len(self.presentes) >= self.capacidade   # Retorna True se a mesa estiver cheia
    
    def esta_vazia(self):
        """Verifica se a mesa está vazia."""
        with self.mutex:    # Protege a seção crítica
            return len(self.presentes) == 0 # Retorna True se a mesa estiver vazia
    
    def get_status(self):   
        """Retorna status atual da mesa."""
        with self.mutex:    # Protege a seção crítica
            return {    
                'presentes_na_mesa': len(self.presentes),
                'capacidade': self.capacidade,
                'total_processados': self.total_presentes_processados,
                'ocupacao_percentual': (len(self.presentes) / self.capacidade) * 100
            }

class ProdutorPresentes(threading.Thread):
    """
    ANALOGIA: Uma thread que simula um processo PRODUTOR independente.
    Gera "trabalho" (presentes) em paralelo com o jogo principal e outras threads.
    """
    
    def __init__(self, esteira_id, gerenciador_mesa, fila_presentes_visuais, intervalo_inicial=3.0):
        super().__init__()
        self.esteira_id = esteira_id    # Identificador da esteira
        self.gerenciador_mesa = gerenciador_mesa    # Referência ao gerenciador de mesa
        self.fila_presentes_visuais = fila_presentes_visuais  # Fila para comunicar com o jogo
        self.intervalo_producao = intervalo_inicial # Intervalo inicial de produção de presentes
        self.running = True # Flag para controlar a execução da thread
        self.daemon = True  # Permite que a thread seja finalizada quando o programa principal terminar
        # Contador de presentes criados por esta esteira
        # Isso é útil para identificar os presentes criados por cada esteira.
        self.presentes_criados = 0 # Contador de presentes criados
        
    def run(self):  
        """
        Loop principal da thread produtora. Continua produzindo
        enquanto 'self.running' for True.
        """
        while self.running:     
            try:
                # ANALOGIA: time.sleep() simula o tempo que um processo
                # leva para realizar um trabalho ou esperar por um evento de E/S.
                time.sleep(self.intervalo_producao)
                
                if self.running:  # Verifica novamente após sleep
                    self.produzir_presente()    
                    
            except Exception as e:  # Captura qualquer exceção que ocorra durante a produção
                print(f"[ERRO] Thread produtora {self.esteira_id}: {e}")
                break
    
    def produzir_presente(self):    
        """
        Cria um novo presente e tenta adicioná-lo ao sistema.
        """
        presente_data = { # Dados do presente a ser criado
            'id': f"presente_{self.esteira_id}_{self.presentes_criados}",
            'esteira_origem': self.esteira_id,
            'timestamp': time.time(),
            'tipo': random.choice(['presente_visual_1', 'presente_visual_2', 'presente_visual_3', 'presente_visual_4'])
        }
        self.presentes_criados += 1 # Incrementa o contador de presentes criados
        # Coloca o presente na fila para o jogo processar visualmente
        try:    # Tenta adicionar o presente à fila de presentes visuais
            self.fila_presentes_visuais.put(presente_data, block=False) 
            print(f"[PRODUTOR {self.esteira_id}] Presente #{self.presentes_criados} criado")
        except: # Se a fila de presentes visuais estiver cheia, não consegue adicionar
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
    ANALOGIA: Um escalonador que ajusta a dificuldade do jogo.
    Nesse caso, a analogia se refere ao escalonamento de processos
    em um sistema operacional, onde o escalonador decide quando e como
    os processos devem ser executados. Aqui, o escalonador ajusta a
    dificuldade do jogo aumentando a velocidade de produção dos presentes
    e a taxa de spawn, simulando o aumento de carga no sistema.
    Ajustável.
    """
    
    def __init__(self, produtores): # Recebe a lista de produtores (esteiras)
        self.produtores = produtores    # Lista de threads produtoras
        self.running = True   # Flag para controlar a execução do escalonador
        self.nivel_dificuldade = 1  # Nível de dificuldade atual do jogo
        self.velocidade_queda_atual = 2.0   # Velocidade de queda dos presentes
        self.taxa_spawn_atual = 2000    # Intervalo de spawn dos presentes (em milissegundos)
        self.incremento_velocidade_queda = 0.2  # Incremento na velocidade de queda a cada nível
        self.fator_aumento_spawn = 0.95 # Fator de redução do intervalo de spawn a cada nível
        
    def aumentar_nivel(self):
        """Ajusta a dificuldade do jogo aumentando velocidade de produção."""
        self.nivel_dificuldade += 1 # Incrementa o nível de dificuldade
        
        for produtor in self.produtores:    # Para cada produtor (esteira)
            if produtor.is_alive():     # Se a thread produtora ainda está ativa
                produtor.acelerar_producao(0.9) # Fica 10% mais rápido
        # Aumenta a velocidade de queda e reduz o intervalo de spawn
        self.velocidade_queda_atual += self.incremento_velocidade_queda
        self.taxa_spawn_atual *= self.fator_aumento_spawn
        
        # Garante que o tempo de spawn não fique rápido demais
        self.taxa_spawn_atual = max(500, self.taxa_spawn_atual)
        
        print(f"[ESCALONADOR] Nível {self.nivel_dificuldade} alcançado! Dificuldade aumentada!")
        print(f"--> Nova velocidade de queda: {self.velocidade_queda_atual:.1f}")
        print(f"--> Novo intervalo de spawn: {self.taxa_spawn_atual:.0f}ms")

    def parar(self):
        """Para o escalonador."""
        self.running = False

class GameMechanics:
    """
    Classe principal que integra todas as mecânicas de SO no jogo.
    """
    
    def __init__(self):
        self.gerenciador_mesa = GerenciadorMesa()   # 
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
        self.nivel_objetivo = 100 # para o próximo nível de dificuldade
        
    def iniciar_sistema(self):
        """Inicia todas as threads e o sistema de mecânicas."""
        if not self.iniciado:
            print("[SISTEMA] Iniciando mecânicas de SO...")
            
            # Inicia threads produtoras
            for produtor in self.produtores:
                produtor.start()
            
            # Inicia escalonador
            # self.escalonador.iniciar()
            
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
            # self.escalonador.parar()
            
            self.iniciado = False
            print("[SISTEMA] Sistema parado!")
    # (NOVO) Método para verificar e aplicar o level up
    def verificar_levelup(self, elfo):
        if self.pontuacao >= self.nivel_objetivo:
            self.escalonador.aumentar_nivel()
            elfo.aumentar_capacidade(10)
            # Define o próximo objetivo de pontuação
            self.nivel_objetivo += 100

    # (NOVO) Método para verificar a condição de derrota
    def verificar_derrota(self):
        # Evita a derrota no início do jogo quando a pontuação é 0
        if self.pontuacao <= 0:
            return False
        
        penalidade_total = self.presentes_perdidos * 10
        limite_derrota = self.pontuacao * 2
        if self.pontuacao != 0:     # condição para evitar derrota logo no início
            if penalidade_total >= limite_derrota:
                return True
            return False
        else:
            return False
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
    
    def elfo_tentar_coletar(self, elfo):
        """
        Simula o processamento de um presente da mesa.
        Retorna True e incrementa a pontuação se a mesa não estava vazia.
        """
        # Primeiro, verificamos se a mesa lógica tem algum item para ser processado.
        if not self.gerenciador_mesa.esta_vazia():
            # Se não está vazia, removemos o item (não importa qual seja).
            self.gerenciador_mesa.remover_presente()
            # E então, garantidamente, adicionamos a pontuação.
            self.pontuacao += 10
            self.verificar_levelup(elfo)
            return True
        # Se a mesa já estava vazia, não faz nada.
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
    

