# entities.py
# Define as classes que representam os "atores" visuais e interativos do jogo.
# como elfo, esteiras, mesa e os presentes que caem.

from ..settings import PASTA_IMAGENS, FONTE_PATH, VERDE_ESCURO, VERDE_CLARO, FONTE_BOLD_PATH, VERMELHO
import os       # Importa o módulo os para manipulação de caminhos de arquivos
import pygame   #   Importa o Pygame para manipulação de gráficos e eventos
import threading    # Importa threading para criar threads de geração de presentes
import random   # Importa random para gerar presentes aleatórios
import math # Importa math para cálculos matemáticos, como seno para animação

class Esteira(pygame.sprite.Sprite):
    """
    Representa o jogador.
    ANALOGIA: Atua como o processo CONSUMIDOR, que retira itens das esteiras
    e os coloca no buffer (Mesa). Também inicia o consumo do buffer (processamento).
    """
    def __init__(self, position, size=(200, 200)):
        """
        position (tuple): Posição inicial do sprite (x, y).
        size (tuple): Tamanho para reescalar os frames da esteira.
        """
        super().__init__()

        # --- Carregamento das Imagens ---
        original_frame_1 = pygame.image.load(os.path.join(PASTA_IMAGENS, "esteira_frame_1.png")).convert_alpha()
        original_frame_2 = pygame.image.load(os.path.join(PASTA_IMAGENS, "esteira_frame_2.png")).convert_alpha()
        # Reescala as imagens para o novo tamanho fornecido
        frame_1 = pygame.transform.scale(original_frame_1, size=(200, 200))
        frame_2 = pygame.transform.scale(original_frame_2, size=(200, 200))
        # Armazena os frames já reescalados na lista
        self.frames = [frame_1, frame_2]    #   Lista de frames da animação da esteira
        self.frame_index = 0    #   Índice do frame atual da animação
        self.image = self.frames[self.frame_index]  #   Define a imagem inicial como o primeiro frame
        self.rect = self.image.get_rect(topleft=position)   #   Retângulo do sprite, usado para posicionamento e colisão
        # --- Controle da Animação ---
        self.animation_speed_ms = 200   # Tempo em milissegundos entre cada frame da animação
        self.last_update = pygame.time.get_ticks()  # Marca o tempo do último update da animação
        # --- Estado da Esteira ---
        self.ligada = True  #   Indica se a esteira está ligada ou não. Se desligada, não anima.

    def animate(self):
        """Controla a lógica de troca de frames da animação."""
        if not self.ligada:
            return
        now = pygame.time.get_ticks()   #   Obtém o tempo atual em milissegundos
        if now - self.last_update > self.animation_speed_ms:    #   Verifica se é hora de trocar o frame
            self.last_update = now  #   Atualiza o tempo do último frame
            self.frame_index = (self.frame_index + 1) % len(self.frames)    #   Incrementa o índice do frame, voltando ao início se necessário
            self.image = self.frames[self.frame_index]  #   Atualiza a imagem do sprite com o novo frame

    def update(self):
        """Método de atualização do sprite, chamado uma vez por frame."""
        self.animate()  # Chama o método de animação para atualizar o frame atual
    
    def ligar(self):
        """Liga a animação da esteira."""
        self.ligada = True  #   Permite que a animação seja executada

    def desligar(self):
        """Desliga a animação da esteira."""
        self.ligada = False #   Impede que a animação seja executada, mantendo o frame atual


class Elfo(pygame.sprite.Sprite):
    """
    Representa o jogador.
    ANALOGIA: Atua como o processo CONSUMIDOR, que retira itens das esteiras
    e os coloca no buffer (Mesa). Também inicia o consumo do buffer (processamento).
    O Elfo pode se mover entre posições fixas (representando as esteiras e a mesa).
    Possui uma capacidade de carga limitada para carregar presentes.
    Pode carregar e descarregar presentes, além de aumentar sua capacidade de carga.
    """
    def __init__(self, positions, start_index=0):
        """
        Inicializa o Elfo com uma imagem, posições possíveis e um índice inicial.
        Args:
            positions (list): Lista de tuplas representando as posições possíveis do Elfo.
            start_index (int): Índice inicial na lista de posições.
        """
        super().__init__()

        # --- Carregamento da Imagem ---
        self.image = pygame.image.load(os.path.join(PASTA_IMAGENS, "elfo.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))

        # --- Lógica de Posição ---
        self.positions = positions  # Armazena a lista de posições possíveis
        self.position_index = start_index  # Guarda o índice da posição atual

        # Define o retângulo do sprite e o posiciona no ponto inicial
        # A posição inicial é baseada no índice fornecido
        self.rect = self.image.get_rect(center=self.positions[self.position_index])

        self.capacidade_carga = 10  #   Capacidade máxima de carga do Elfo
        self.presentes_carregados = 0   #   Contador de presentes atualmente carregados pelo Elfo
        self.font_carga = pygame.font.Font(FONTE_BOLD_PATH, 20) # Fonte para o texto de carga
        self.texto_carga = None # Superfície para o texto de carga
        self.posicao_texto_carga = None # Posição do texto de carga em relação ao retângulo do sprite

    def move(self, direction):  
        """
        Move o Elfo para a próxima posição fixa na direção especificada.

        Args:
            direction (str): A direção do movimento ("left" ou "right").
        """
        if direction == "right":
            # Verifica se o elfo NÃO está na última posição (limite direito)
            if self.position_index < len(self.positions) - 1:
                self.position_index += 1
                print(f"Moveu para a direita. Novo índice: {self.position_index}")

        elif direction == "left":
            # Verifica se o elfo NÃO está na primeira posição (limite esquerdo)
            if self.position_index > 0:
                self.position_index -= 1
                print(f"Moveu para a esquerda. Novo índice: {self.position_index}")
        
        # Atualiza a posição do retângulo do sprite para a nova posição central
        self.rect.center = self.positions[self.position_index]

    def carregar_presente(self):
        """Incrementa a contagem de presentes carregados se não atingir a capacidade."""
        if self.presentes_carregados < self.capacidade_carga:
            self.presentes_carregados += 1
            self._atualizar_texto_carga()

    def descarregar_presente(self):
        """Decrementa a contagem de presentes carregados."""
        if self.presentes_carregados > 0:
            self.presentes_carregados -= 1
            self._atualizar_texto_carga()

    def _atualizar_texto_carga(self):
        """Atualiza a superfície do texto que indica a quantidade de carga."""
        cor_texto = (0, 200, 0) # Verde para vazio/pouco carregado
        if self.presentes_carregados == self.capacidade_carga:
            cor_texto = (255, 0, 0)   # Vermelho para cheio
        elif self.presentes_carregados >= self.capacidade_carga * 0.75:
            cor_texto = (255, 255, 0) # Amarelo para quase cheio

        texto = f"{self.presentes_carregados}"  # Quantidade de presentes carregados
        self.texto_carga = self.font_carga.render(texto, True, cor_texto)
        self.posicao_texto_carga = (self.rect.centerx - self.texto_carga.get_width() // 2,
                                    self.rect.top - self.texto_carga.get_height() - 5)
    def desenhar_carga(self, surface):  
        """Desenha o indicador de carga sobre a cabeça do elfo."""
        if self.presentes_carregados > 0 and self.texto_carga is not None:
            # Desenha o texto de carga acima do Elfo
            pos_x = self.rect.centerx - self.texto_carga.get_width() // 2
            pos_y = self.rect.top - self.texto_carga.get_height() - 5
            surface.blit(self.texto_carga, (pos_x, pos_y))

    def aumentar_capacidade(self, aumento):
        """Aumenta a capacidade de carga do elfo."""
        self.capacidade_carga += aumento
        print(f"[LEVEL UP] Capacidade do elfo aumentada para: {self.capacidade_carga}")
        
    def update(self):   #   Método de atualização do sprite, chamado uma vez por frame.
        """Atualiza o Elfo, incluindo a animação do texto de carga."""
        self._atualizar_texto_carga() # Garante que o texto seja atualizado a cada frame

    def draw(self, surface):    #   Método de desenho, chamado uma vez por frame.
        super().draw(surface)   # Desenha o sprite do Elfo na superfície fornecida
        if self.texto_carga is not None and self.posicao_texto_carga is not None:
            surface.blit(self.texto_carga, self.posicao_texto_carga)

class Presente(pygame.sprite.Sprite):   
    """
    Representa o item de "trabalho" do jogo. Produzido e consumido.
    """

    def __init__(self, esteira, game_mechanics, fall_speed=1, ):
        """
        Args:
            esteira (Esteira): A esteira de onde o presente será gerado.
            fall_speed (int): A velocidade inicial de queda do presente.
        """
        super().__init__()  
        self.esteira = esteira  # Referência à esteira de onde o presente foi gerado
        self.game_mechanics = game_mechanics  # Referência ao gerenciador de mecânicas do jogo
        self.fall_speed = fall_speed    # Velocidade de queda do presente
        # --- Carregamento da Imagem do Presente ---
        tipos_presente = ["presente_visual_1.png", "presente_visual_2.png", "presente_visual_3.png", "presente_visual_4.png"]
        tipo_escolhido = random.choice(tipos_presente)  # Escolhe aleatoriamente um tipo de presente
        # Tenta carregar a imagem do presente escolhido
        try:
            self.image = pygame.image.load(os.path.join(PASTA_IMAGENS, tipo_escolhido)).convert_alpha()
        except:
            # Fallback se a imagem não existir
            self.image = pygame.Surface((80, 80))
            self.image.fill((255, 0, 0))  # Vermelho como fallback
            
        self.image = pygame.transform.scale(self.image, (80, 80))  # Tamanho maior para melhor visibilidade

        # Define o retângulo do sprite e posiciona acima da esteira
        self.rect = self.image.get_rect(center=(self.esteira.rect.centerx, self.esteira.rect.top+30))

    def update(self):   
        """Atualiza a posição do presente, fazendo-o cair."""
        self.rect.y += self.fall_speed  # Move o presente para baixo pela velocidade de queda

        if self.rect.top > pygame.display.get_surface().get_height():
            # Avisa o game_mechanics sobre a perda
            self.game_mechanics.presentes_perdidos += 1
            print(f"[QUEDA] Um presente caiu no chão! Total de perdidos: {self.game_mechanics.presentes_perdidos}")
            # E então se autodestrói
            self.kill()


class GeradorPresentes(threading.Thread):
    """
    Classe responsável por gerar presentes em uma esteira específica.
    A geração de presentes é controlada por uma thread para não bloquear o jogo.
    """
    def __init__(self, esteira, fall_speed=1, spawn_rate=1000):
        super().__init__()
        self.esteira = esteira  # Referência à esteira onde os presentes serão gerados
        self.fall_speed = fall_speed    # Velocidade de queda dos presentes
        self.spawn_rate = spawn_rate  # Tempo em milissegundos entre cada geração de presente
        self.running = True # Flag para controlar a execução da thread

    def run(self):
        """Método que executa a thread de geração de presentes."""
        while self.running:     
            pygame.time.delay(self.spawn_rate)  # Espera pelo tempo de spawn definido
            if self.running:  # Verifica se a thread ainda está ativa
                presente = Presente(self.esteira, fall_speed=self.fall_speed)
                self.esteira.add(presente)  # Adiciona o presente ao grupo da esteira

    def stop(self):
        """Método para parar a thread de geração de presentes."""
        self.running = False    # Para parar a thread
        self.join() # Aguarda a thread terminar antes de continuar


class MesaDePresentes(pygame.sprite.Sprite):
    """
    Representa a interface VISUAL do recurso compartilhado.
    Seu estado (número de presentes visuais) reflete o estado do
    'GerenciadorMesa' lógico.
    """
    def __init__(self, position, capacidade=3):
        super().__init__()
        TAMANHO_VISUAL_PRESENTE = (100, 100)
        self.original_image = pygame.image.load(os.path.join(PASTA_IMAGENS, "mesadeembrulhos.png")).convert_alpha()
        self.image_base = pygame.transform.scale(self.original_image, size=(150, 80))
        self.visuais_presentes = []
        # Usa presente_visual_1.png até presente_visual_4.png na mesa
        tipos_presente = ["presente_visual_1.png", "presente_visual_2.png", "presente_visual_3.png", "presente_visual_4.png"]
        for tipo in tipos_presente:
            try:
                # Carrega a imagem original do presente
                original_img = pygame.image.load(os.path.join(PASTA_IMAGENS, tipo)).convert_alpha()
                # Reescala a imagem para o novo tamanho
                scaled_img = pygame.transform.scale(original_img, TAMANHO_VISUAL_PRESENTE)
                # Adiciona a imagem já reescalada à lista
                self.visuais_presentes.append(scaled_img)
            except:
                # Fallback se a imagem não existir
                fallback_img = pygame.Surface(TAMANHO_VISUAL_PRESENTE)
                fallback_img.fill((255, 0, 0))  # Vermelho como fallback
                self.visuais_presentes.append(fallback_img)
        self.capacidade = capacidade
        self.itens_visuais = []
        
        # --- Variáveis para Processamento Automático ---
        self.processamento_ativo = True  # Se a mesa deve processar automaticamente
        self.tempo_processamento = 2000  # Tempo em ms para processar um presente (2 segundos para teste)
        self.ultimo_processamento = 0  # Inicializa com 0 para começar imediatamente
        self.presentes_processados_total = 0
        
        # --- Estado visual do processamento ---
        self.processando = False
        self.tempo_inicio_processamento = 0
        self.posicoes_slots = [(-5, -40), (35, -40), (75, -40)] # Ajuste essas posições se necessário
        self.image = self.image_base.copy()
        self.rect = self.image.get_rect(center = position)

    def _redesenhar_superficie(self):
        """
        Método privado para atualizar a imagem da mesa com os presentes atuais.
        É chamado sempre que um item é adicionado ou removido.
        """
        self.image = self.image_base.copy()
        # Desenha os presentes na mesa
        for i, presente_img in enumerate(self.itens_visuais):
            # Garante que não tentemos acessar um slot que não existe
            if i < len(self.posicoes_slots):
                posicao_no_slot = self.posicoes_slots[i]
                # Se está processando e é o primeiro presente, adiciona efeito visual
                if self.processando and i == 0:
                    # Cria uma cópia da imagem do presente com transparência
                    presente_processando = presente_img.copy()
                    presente_processando.set_alpha(150)  # Torna semi-transparente
                    self.image.blit(presente_processando, posicao_no_slot)
                    # Adiciona um pequeno texto indicando processamento
                    try:
                        font_pequena = pygame.font.Font(None, 16)
                        texto_proc = font_pequena.render("PROC", True, (255, 255, 0))  # Amarelo
                        self.image.blit(texto_proc, (posicao_no_slot[0] + 10, posicao_no_slot[1] - 15))
                    except:
                        pass  # Se não conseguir carregar fonte, ignora o texto
                else:
                    self.image.blit(presente_img, posicao_no_slot)

    def adicionar_presente_visual(self):
        """
        Adiciona a aparência de um novo presente à mesa - se houver espaço
        retorna True se sucesso
        """
        if len(self.itens_visuais) < self.capacidade:   # Verifica se há espaço na mesa
            novo_presente_img = random.choice(self.visuais_presentes) # Escolhe aleatoriamente uma imagem de presente
            self.itens_visuais.append(novo_presente_img)    
            self._redesenhar_superficie()
            print(f"Visual de presente adicionado. Itens na mesa: {len(self.itens_visuais)}")
            return True
        else:
            print("Visual da mesa já está cheio.")
            return False

    def remover_presente_visual(self):
        """
        Remove a aparência de um presente da mesa.
        Retorna True se bem-sucedido, False caso contrário.
        """
        if self.itens_visuais:  # Verifica se há presentes na mesa
            self.itens_visuais.pop(0)   # Remove o primeiro presente (FIFO)
            
            self._redesenhar_superficie()   
            print(f"Visual de presente removido. Itens na mesa: {len(self.itens_visuais)}")
            return True
        else:
            print("Visual da mesa já está vazio.")
            return False

    def processar_presente(self):   
        """
        Processa (remove) um presente da mesa, simulando o trabalho de embrulho.
        Retorna True se processou um presente, False se mesa vazia.
        """
        if self.itens_visuais and not self.processando:
            self.processando = True
            self.tempo_inicio_processamento = pygame.time.get_ticks()
            print(f"[MESA] Iniciando processamento de presente...")
            return True
        return False
    
    def finalizar_processamento_visual(self):
        """
        Finaliza o processamento VISUAL de um presente.
        A lógica de liberação do semáforo é externa.
        """
        if self.processando and self.itens_visuais:
            self.itens_visuais.pop(0)  # Remove o primeiro presente (FIFO)
            self.presentes_processados_total += 1   # Contador de presentes processados
            self.processando = False    # Reseta o estado de processamento
            self._redesenhar_superficie()
            print(f"[MESA VISUAL] Presente processado! Restam: {len(self.itens_visuais)}, Total processados: {self.presentes_processados_total}")
            # Não chama mais a lógica de remoção aqui
            return True 
        elif self.processando:      # Se estava processando mas não há itens visuais
            self.processando = False    # Reseta o estado de processamento
            self._redesenhar_superficie()   # Atualiza a imagem da mesa
        return False

    def verificar_processamento_concluido(self):
        """
        Verifica se o tempo de processamento de um item terminou.
        Retorna True se um item acabou de ser processado, False caso contrário.
        Este método é chamado pelo loop principal do jogo.
        """
        if self.processando:
            current_time = pygame.time.get_ticks()
            tempo_decorrido = current_time - self.tempo_inicio_processamento
            if tempo_decorrido >= self.tempo_processamento:
                # O processamento terminou, mas não faz a remoção aqui.
                # Apenas sinaliza que deve ser feito.
                return True
        return False

    def update(self):
        """
        Atualiza a mesa, focando no início do processamento automático.
        A finalização será tratada pelo loop principal do jogo.
        """
        current_time = pygame.time.get_ticks()
        # Se o processamento automático está ativo, verifica se deve processar
        if (self.processamento_ativo and    #   Se o processamento automático está ativo
              len(self.itens_visuais) > 0 and #  # Se há itens visuais na mesa
              not self.processando):    # Se não está processando atualmente
            
            tempo_desde_ultimo = current_time - self.ultimo_processamento
            if tempo_desde_ultimo >= self.tempo_processamento:
                if self.processar_presente():
                    # No processamento automático, o último processamento só é atualizado
                    # quando o item é efetivamente removido no game_loop.
                    pass
        
        # Se não há presentes, reseta o timer para evitar processamento imediato
        # ao adicionar o próximo item.
        elif len(self.itens_visuais) == 0 and not self.processando:
            self.ultimo_processamento = current_time


class ContadorDePresentes(pygame.sprite.Sprite):
    """
    Classe que representa um contador visual de presentes com um ícone animado.
    O ícone do presente pulsa (aumenta e diminui de tamanho) suavemente.
    """
    def __init__(self, position, font_size=30):
        super().__init__()
        self.position = position # Posição do canto superior esquerdo do contador
        self.font = pygame.font.Font(FONTE_BOLD_PATH, font_size)
        self.count = 0

        # --- Carregamento e Configuração da Imagem do Ícone ---
        # Carrega a imagem original do ícone UMA VEZ e já redimensiona para 100x100
        self.presente_original_img = pygame.image.load(os.path.join(PASTA_IMAGENS, "presente_visual_4.png")).convert_alpha()
        self.presente_original_img = pygame.transform.scale(self.presente_original_img, (100, 100))
        self.presente_original_size = self.presente_original_img.get_size()
        # Esta superfície guardará o ícone redimensionado a cada frame
        self.presente_animado_img = self.presente_original_img

        # --- Parâmetros da Animação de Pulsar ---
        self.pulse_speed = 3.0  # Quão rápido o ícone pulsa
        self.pulse_amplitude = 0.1  # Quão "forte" é o pulso (0.1 = 10% de variação de tamanho)

        # Chama o método para criar a imagem inicial do sprite
        self._redesenhar_superficie()

    def incrementar(self):
        """Incrementa o contador de presentes e atualiza o texto."""
        self.count += 1
        # Apenas redesenha a superfície. O update cuidará da animação.
        self._redesenhar_superficie()

    def _redesenhar_superficie(self):
        """
        Método privado que combina o texto e o ícone do presente em uma única
        superfície (self.image).
        """
        # Renderiza o texto
        texto_surface = self.font.render(f"Presentes: {self.count}", True, VERMELHO)
        texto_rect = texto_surface.get_rect()

        # Pega a imagem do presente já animada (pelo método update)
        presente_rect = self.presente_animado_img.get_rect()

        # Calcula o tamanho da nova superfície combinada
        padding = 10 # Espaço entre o texto e o ícone
        total_width = texto_rect.width + padding + presente_rect.width
        total_height = max(texto_rect.height, presente_rect.height)

        # Cria a superfície final com fundo transparente
        self.image = pygame.Surface((total_width, total_height), pygame.SRCALPHA)

        # Desenha o texto e o ícone na nova superfície
        self.image.blit(texto_surface, (0, (total_height - texto_rect.height) // 2))
        self.image.blit(self.presente_animado_img, (texto_rect.width + padding, (total_height - presente_rect.height) // 2))

        # Atualiza o retângulo principal do sprite
        self.rect = self.image.get_rect(topleft=self.position)

    def update(self):
        """
        Atualiza a animação do ícone do presente a cada frame.
        """
        # Calcula o fator de escala usando uma função seno para criar a pulsação
        # pygame.time.get_ticks() retorna o tempo em milissegundos
        tempo = pygame.time.get_ticks() / 1000.0  # Converte para segundos
        scale_factor = 1.0 + math.sin(tempo * self.pulse_speed) * self.pulse_amplitude

        # Calcula as novas dimensões do ícone
        novo_width = int(self.presente_original_size[0] * scale_factor)
        novo_height = int(self.presente_original_size[1] * scale_factor)

        # Redimensiona a imagem original
        self.presente_animado_img = pygame.transform.scale(self.presente_original_img, (novo_width, novo_height))

        # Chama o método para redesenhar a superfície combinada com o ícone no novo tamanho
        self._redesenhar_superficie()