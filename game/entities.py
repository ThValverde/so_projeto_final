# game/entities.py
# Define as classes que representam os "atores" do jogo, incluindo as threads.

from ..settings import PASTA_IMAGENS, FONTE_PATH, VERDE_ESCURO, VERDE_CLARO
import os
import pygame

class Esteira(pygame.sprite.Sprite):
    """
    Representa uma esteira animada que produz presentes.
    A animação alterna entre duas texturas para simular movimento.
    """
    # AQUI ESTÁ A CORREÇÃO: Adicionamos o parâmetro 'size' ao __init__
    def __init__(self, position, size=(400, 120)):
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
