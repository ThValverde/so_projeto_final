# ui/screens.py
# Define as classes para as telas de carregamento e final.

from ..settings import LARGURA_TELA, ALTURA_TELA, PASTA_IMAGENS
import pygame
import os

class MenuBackground:
    """Classe para o fundo do menu principal."""
    
    def __init__(self):
        self.image = pygame.image.load(os.path.join(PASTA_IMAGENS, "menubackground.png"))
        self.image = pygame.transform.scale(self.image, (LARGURA_TELA, ALTURA_TELA))
        self.rect = self.image.get_rect()

    def draw(self, screen):
        """Desenha o fundo na tela."""
        screen.blit(self.image, self.rect)
class LoadingScreenToGame:
    """Classe para a tela de carregamento do jogo.
        Desenhará uma sequência de imagens de carregamento
        durante um tempo, enquanto o áudio explicativo é reproduzido.
        A tela de carregamento é exibida antes do início do jogo,
        permitindo que o jogador veja que o jogo está sendo carregado.
        O intervalo de exibição de cada imagem é específico, dessa maneira
        cada imagem tera um tempo de exibição diferente.
    """

    def __init__(self, images, durations, audio_path):
        """
        images: lista de caminhos para imagens de carregamento.
        durations: lista de tempos de exibição (em segundos) para cada imagem.
        audio_path: caminho para o arquivo de áudio explicativo.
        """
        self.images = [pygame.transform.scale(pygame.image.load(img), (LARGURA_TELA, ALTURA_TELA)) for img in images]
        self.durations = durations
        self.audio_path = audio_path
        self.current_index = 0
        self.start_time = None
        self.finished = False

    def start(self):
        """Inicia a tela de carregamento e o áudio."""
        self.current_index = 0
        self.start_time = pygame.time.get_ticks()
        self.finished = False
        pygame.mixer.music.load(self.audio_path)
        pygame.mixer.music.play()

    def update(self):
        """Atualiza o índice da imagem de acordo com o tempo."""
        if self.finished or self.start_time is None:
            return

        elapsed = (pygame.time.get_ticks() - self.start_time) / 1000  # segundos
        total = 0
        for i, duration in enumerate(self.durations):
            total += duration
            if elapsed < total:
                self.current_index = i
                break
        else:
            self.finished = True
            pygame.mixer.music.stop()

    def draw(self, screen):
        """Desenha a imagem de carregamento atual."""
        if not self.finished and self.images:
            screen.blit(self.images[self.current_index], (0, 0))

class GameBackground:
    """Classe para o fundo do jogo."""
    
    def __init__(self):
        self.image = pygame.image.load("assets/images/gamebackground.png")
        self.image = pygame.transform.scale(self.image, (LARGURA_TELA, ALTURA_TELA))
        self.rect = self.image.get_rect()

    def draw(self, screen):
        """Desenha o fundo na tela."""
        screen.blit(self.image, self.rect)

class GameOverScreen:
    """Classe para a tela de Game Over."""
    
    def __init__(self):
        self.image = pygame.image.load("assets/images/gameover.png")
        self.image = pygame.transform.scale(self.image, (LARGURA_TELA, ALTURA_TELA))
        self.rect = self.image.get_rect()

    def draw(self, screen):
        """Desenha a tela de Game Over na tela."""
        screen.blit(self.image, self.rect)

class VictoryScreen:
    """Classe para a tela de vitória."""
    
    def __init__(self):
        self.image = pygame.image.load("assets/images/victory.png")
        self.image = pygame.transform.scale(self.image, (LARGURA_TELA, ALTURA_TELA))
        self.rect = self.image.get_rect()

    def draw(self, screen):
        """Desenha a tela de vitória na tela."""
        screen.blit(self.image, self.rect)


class EndScreen:
    """Classe para a tela de fim de jogo."""
    
    def __init__(self):
        self.image = os.path.join(PASTA_IMAGENS, "endscreen.png")
        self.image = pygame.image.load(self.image)
        self.image = pygame.transform.scale(self.image, (LARGURA_TELA, ALTURA_TELA))
        self.rect = self.image.get_rect()

    def draw(self, screen):
        """Desenha a tela de fim de jogo na tela."""
        screen.blit(self.image, self.rect)
