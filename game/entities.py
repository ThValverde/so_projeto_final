# game/entities.py
# Define as classes que representam os "atores" do jogo, incluindo as threads.

from ..settings import PASTA_IMAGENS, FONTE_PATH, VERDE_ESCURO, VERDE_CLARO
import os
import pygame
import threading
import random

class Esteira(pygame.sprite.Sprite):
    """
    Representa uma esteira animada que produz presentes.
    A animação alterna entre duas texturas para simular movimento.
    """
    # AQUI ESTÁ A CORREÇÃO: Adicionamos o parâmetro 'size' ao __init__
    def __init__(self, position, size=(200, 200)):
        """
        Args:
            position (tuple): A posição (x, y) do canto superior esquerdo da esteira.
            size (tuple): O novo tamanho (largura, altura) para a imagem da esteira.
        """
        super().__init__()

        # --- Carregamento e Reescalonamento dos Frames ---
        
        # Carrega as imagens originais
        original_frame_1 = pygame.image.load(os.path.join(PASTA_IMAGENS, "esteira_frame_1.png")).convert_alpha()
        original_frame_2 = pygame.image.load(os.path.join(PASTA_IMAGENS, "esteira_frame_2.png")).convert_alpha()
        
        # Reescala as imagens para o novo tamanho fornecido
        frame_1 = pygame.transform.scale(original_frame_1, size=(200, 200))
        frame_2 = pygame.transform.scale(original_frame_2, size=(200, 200))

        # Armazena os frames já reescalados na lista
        self.frames = [frame_1, frame_2]
        self.frame_index = 0

        # O resto do código funciona normalmente com as imagens já no novo tamanho
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=position)

        # --- Controle da Animação ---
        self.animation_speed_ms = 200 
        self.last_update = pygame.time.get_ticks()

        # --- Estado da Esteira ---
        self.ligada = True

    def animate(self):
        """Controla a lógica de troca de frames da animação."""
        if not self.ligada:
            return
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed_ms:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]

    def update(self):
        """Método de atualização do sprite, chamado uma vez por frame."""
        self.animate()
    
    def ligar(self):
        """Liga a animação da esteira."""
        self.ligada = True

    def desligar(self):
        """Desliga a animação da esteira."""
        self.ligada = False


class Elfo(pygame.sprite.Sprite):
    """
    Representa o jogador (Elfo), que se move entre posições fixas.
    """
    def __init__(self, positions, start_index=0):
        """
        Args:
            positions (list): Uma lista de tuplas (x, y) representando as posições fixas.
            start_index (int): O índice da lista 'positions' onde o Elfo deve começar.
        """
        super().__init__()

        # --- Carregamento da Imagem ---
        # Carrega a imagem do Elfo. Altere o nome do arquivo se necessário.
        self.image = pygame.image.load(os.path.join(PASTA_IMAGENS, "elfo.png")).convert_alpha()
        # Você pode reescalar a imagem se precisar, exemplo:
        self.image = pygame.transform.scale(self.image, (100, 100))

        # --- Lógica de Posição ---
        self.positions = positions  # Armazena a lista de posições possíveis
        self.position_index = start_index  # Guarda o índice da posição atual

        # Define o retângulo do sprite e o posiciona no ponto inicial
        # Usar 'center' ajuda a posicionar o sprite pelo seu centro
        self.rect = self.image.get_rect(center=self.positions[self.position_index])

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

    def update(self):
        """
        O método de atualização do sprite.
        Por enquanto, não precisa fazer nada, pois o movimento é controlado por eventos.
        """
        pass


class Presente(pygame.sprite.Sprite):
    """
    Representa um presente que pode ser coletado pelo Elfo.
    O presente é gerado em uma posição acima de uma esteira e cai em direção ao chão.
    Possui uma taxa de aparecimento controlada por uma thread.
    O jogo deve garantir que os presentes sejam gerados um por vez
    e alternando entre as esteiras.
    A taxa de aprecimento é incrementada até um limite máximo.
    A velocidade de queda é incrementada até um limite máximo.
    """

    def __init__(self, esteira, fall_speed=1):
        """
        Args:
            esteira (Esteira): A esteira de onde o presente será gerado.
            fall_speed (int): A velocidade inicial de queda do presente.
        """
        super().__init__()
        self.esteira = esteira
        self.fall_speed = fall_speed

        # Carrega a imagem do presente
        self.image = pygame.image.load(os.path.join(PASTA_IMAGENS, "presente.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))  # Ajuste o tamanho conforme necessário

        # Define o retângulo do sprite e posiciona acima da esteira
        self.rect = self.image.get_rect(center=(self.esteira.rect.centerx, self.esteira.rect.top - 50))

    def update(self):
        """Atualiza a posição do presente, fazendo-o cair."""
        self.rect.y += self.fall_speed

        # Se o presente sair da tela, remove-o do grupo de sprites
        if self.rect.top > pygame.display.get_surface().get_height():
            self.kill()

class GeradorPresentes(threading.Thread):
    """
    Classe responsável por gerar presentes em uma esteira específica.
    A geração de presentes é controlada por uma thread para não bloquear o jogo.
    """
    def __init__(self, esteira, fall_speed=1, spawn_rate=1000):
        super().__init__()
        self.esteira = esteira
        self.fall_speed = fall_speed
        self.spawn_rate = spawn_rate  # Tempo em milissegundos entre cada geração de presente
        self.running = True

    def run(self):
        """Método que executa a thread de geração de presentes."""
        while self.running:
            pygame.time.delay(self.spawn_rate)
            if self.running:  # Verifica se a thread ainda está ativa
                presente = Presente(self.esteira, fall_speed=self.fall_speed)
                self.esteira.add(presente)  # Adiciona o presente ao grupo da esteira

    def stop(self):
        """Método para parar a thread de geração de presentes."""
        self.running = False
        self.join()

class MesaDePresentes(pygame.sprite.Sprite):
    def __init__(self, position, capacidade=3):
        super().__init__()
        TAMANHO_VISUAL_PRESENTE = (100, 100)
        # --- CORREÇÃO 1: Sintaxe do os.path.join e nome da variável ---
        # A variável foi padronizada para self.image_base
        self.original_image = pygame.image.load(os.path.join(PASTA_IMAGENS, "mesadeembrulhos.png")).convert_alpha()
        
        self.image_base = pygame.transform.scale(self.original_image, size=(150, 80))

        self.visuais_presentes = []
        for i in range (1, 4):
            # Carrega a imagem original do presente
            original_img = pygame.image.load(os.path.join(PASTA_IMAGENS, f"presente_visual_{i}.png")).convert_alpha()
            # Reescala a imagem para o novo tamanho
            scaled_img = pygame.transform.scale(original_img, TAMANHO_VISUAL_PRESENTE)
            # Adiciona a imagem já reescalada à lista
            self.visuais_presentes.append(scaled_img)
        self.capacidade = capacidade
        self.itens_visuais = []

        self.posicoes_slots = [(-5, -40), (35, -40), (75, -40)] # Ajuste essas posições se necessário

        self.image = self.image_base.copy()
        # --- CORREÇÃO 2: Typo em self.image ---
        self.rect = self.image.get_rect(center = position)

    def _redesenhar_superficie(self):
        """
        Método privado para atualizar a imagem da mesa com os presentes atuais.
        É chamado sempre que um item é adicionado ou removido.
        """
        self.image = self.image_base.copy()

        # --- CORREÇÃO AQUI ---
        # Devemos iterar sobre os itens que ESTÃO na mesa (self.itens_visuais),
        # e não sobre todas as aparências possíveis.
        for i, presente_img in enumerate(self.itens_visuais):
            # Garante que não tentemos acessar um slot que não existe
            if i < len(self.posicoes_slots):
                posicao_no_slot = self.posicoes_slots[i]
                self.image.blit(presente_img, posicao_no_slot)

    def adicionar_presente_visual(self):
        """
        Adiciona a aparência de um novo presente à mesa - se houver espaço
        retorna True se sucesso
        """
        if len(self.itens_visuais) < self.capacidade:
            novo_presente_img = random.choice(self.visuais_presentes)
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
        if self.itens_visuais:
            self.itens_visuais.pop(0) 
            
            self._redesenhar_superficie()
            print(f"Visual de presente removido. Itens na mesa: {len(self.itens_visuais)}")
            return True
        else:
            print("Visual da mesa já está vazio.")
            return False

    def update(self):
        """
        O método update não precisa fazer nada ativamente.
        """
        pass