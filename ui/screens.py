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
            images (list): Lista de nomes de arquivos de imagem (ex: ["load1.png", "load2.png"]).
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
        self.audio_path = audio_path

        # Calcula a duração total da animação somando as durações individuais
        self.total_duration = sum(self.durations)

        # Variáveis de estado
        self.current_image_index = 0
        self.start_time = None
        self.finished = True # Começa como finalizado, só fica ativo após chamar start()

    def start(self):
        """Inicia ou reinicia a animação da tela de carregamento."""
        print("Iniciando a tela de carregamento...")
        self.start_time = pygame.time.get_ticks()
        self.current_image_index = 0
        self.finished = False

        # Lógica para tocar o áudio (pronta para o futuro)
        if self.audio_path and os.path.exists(self.audio_path):
            try:
                pygame.mixer.music.load(self.audio_path)
                # play() toca uma vez. play(-1) toca em loop. Usamos play() aqui.
                pygame.mixer.music.play()
            except pygame.error as e:
                print(f"Não foi possível carregar o áudio: {e}")
        else:
            print("Áudio não fornecido ou não encontrado, rodando apenas com o tempo das imagens.")


    def update(self):
        """Atualiza a imagem a ser exibida com base no tempo decorrido."""
        # Se a animação terminou ou não começou, não faz nada
        if self.finished or self.start_time is None:
            return

        # Calcula o tempo que passou desde o início em segundos
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000

        # Verifica se o tempo total da animação já passou
        if elapsed_time >= self.total_duration:
            self.finished = True
            pygame.mixer.music.stop() # Garante que a música pare
            print("Tela de carregamento finalizada.")
            return

        # Lógica para descobrir qual imagem mostrar
        cumulative_time = 0
        for i, duration in enumerate(self.durations):
            cumulative_time += duration
            if elapsed_time < cumulative_time:
                self.current_image_index = i
                break # Encontrou a imagem correta, pode parar o loop

    def draw(self, screen):
        """Desenha a imagem de carregamento atual na tela."""
        # Só desenha se a animação não tiver terminado
        if not self.finished and self.images:
            # Pega a imagem correta da lista
            current_image = self.images[self.current_image_index]
            # Desenha a imagem na tela
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
        self.image = pygame.image.load(os.path.join(PASTA_IMAGENS, "endscreen.png"))
        self.image = pygame.transform.scale(self.image, (LARGURA_TELA, ALTURA_TELA))
        self.rect = self.image.get_rect()

    def draw(self, screen):
        """Desenha a tela final na tela."""
        screen.blit(self.image, self.rect)
    

