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
    """
    Exibe uma sequência de imagens por durações específicas,
    sincronizada com um áudio.
    """

    def __init__(self, images, durations, audio_path=None):
        """
        Args:
            images (list): Lista de nomes de arquivos de imagem (ex: ["loading1.png", "loading2.png, loading3.png"]).
            durations (list): Lista de durações em segundos para cada imagem.
            audio_path (str, optional): Caminho para o arquivo de áudio. Defaults to None.
        """
        # Carrega e escala as imagens para o tamanho da tela
        self.images = [
            pygame.transform.scale(
                pygame.image.load(os.path.join(PASTA_IMAGENS, img)),
                (LARGURA_TELA, ALTURA_TELA)
            ) for img in images
        ]
        self.durations = durations
        
        # O caminho do áudio está pronto para o futuro, mas pode ser None por enquanto
        self.sounds = []
        if audio_path:
            from .. settings import PASTA_AUDIO
            for audio_file in audio_path:
                path = os.path.join(PASTA_AUDIO, audio_file)
                if os.path.exists(path):
                    self.sounds.append(pygame.mixer.Sound(path))
                else:
                    print(f"Áudio {audio_file} não encontrado em {PASTA_AUDIO}.")
                    self.sounds.append(None)
        # Calcula a duração total da animação somando as durações individuais
        self.total_duration = sum(self.durations)

        # Variáveis de estado
        self.current_image_index = -1
        self.start_time = None
        self.finished = True # Começa como finalizado, só fica ativo após chamar start()

    def start(self):
        print("Iniciando a tela de carregamento...")
        self.start_time = pygame.time.get_ticks()
        self.current_image_index = -1
        self.finished = False

    def update(self):
        if self.finished or self.start_time is None:
            return

        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000

        if elapsed_time >= self.total_duration:
            self.finished = True
            pygame.mixer.stop() # Para qualquer som que ainda esteja tocando
            print("Tela de carregamento finalizada.")
            return

        # Descobre o índice da imagem atual
        target_index = 0
        cumulative_time = 0
        for i, duration in enumerate(self.durations):
            cumulative_time += duration
            if elapsed_time < cumulative_time:
                target_index = i
                break

        # (LÓGICA DE ÁUDIO) Se o índice da imagem mudou, toca o novo som
        if target_index != self.current_image_index:
            self.current_image_index = target_index
            # Toca o som correspondente, se ele existir
            if self.current_image_index < len(self.sounds) and self.sounds[self.current_image_index]:
                pygame.mixer.stop() # Para o som anterior
                self.sounds[self.current_image_index].play()

    def draw(self, screen):
        if not self.finished and self.images and self.current_image_index != -1:
            current_image = self.images[self.current_image_index]
            screen.blit(current_image, (0, 0))

class GameBackground:
    """Classe para o fundo do jogo."""
    
    def __init__(self):
        self.image = pygame.image.load(os.path.join(PASTA_IMAGENS, "gamebackground.png"))
        self.image = pygame.transform.scale(self.image, (LARGURA_TELA, ALTURA_TELA))
        self.rect = self.image.get_rect()

    def draw(self, screen):
        """Desenha o fundo na tela."""
        screen.blit(self.image, self.rect)

class EndScreen:
    """Classe para a tela final do jogo."""
    
    def __init__(self):
        self.image = pygame.image.load(os.path.join(PASTA_IMAGENS, "gamebackground.png"))
        self.image = pygame.transform.scale(self.image, (LARGURA_TELA, ALTURA_TELA))
        self.rect = self.image.get_rect()

    def draw(self, screen):
        """Desenha a tela final na tela."""
        screen.blit(self.image, self.rect)
    

