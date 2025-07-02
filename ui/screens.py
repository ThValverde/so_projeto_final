# ui/screens.py
# Define as classes para as telas de carregamento e final.

from ..settings import LARGURA_TELA, ALTURA_TELA, PASTA_IMAGENS 
import pygame   # Importa a biblioteca Pygame para manipulação de gráficos, som e eventos
import os   # Importa a biblioteca os para manipulação de caminhos de arquivos e diretórios

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

    def __init__(self, images, durations, audio_path=None, initial_audio_delay=0.0):
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
        
        self.initial_audio_delay = initial_audio_delay # Armazena o atraso desejado
        self.audio_start_time = 0 # Tempo em que o áudio deveria começar a tocar (start_time + delay)
        self.first_audio_played = False # Flag para garantir que o primeiro áudio só toque uma vez


    def start(self):
        print("Iniciando a tela de carregamento...")
        self.start_time = pygame.time.get_ticks()
        self.current_image_index = -1
        self.finished = False
        self.audio_start_time = self.start_time + (self.initial_audio_delay * 1000) # Convertendo segundos para milissegundos
        self.first_audio_played = False # Reseta a flag para uma nova execução
        
    def update(self):
        if self.finished or self.start_time is None:
            return


        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.start_time) / 1000
        # elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000

        if elapsed_time >= self.total_duration:
            self.finished = True
            pygame.mixer.stop() # Para qualquer som que ainda esteja tocando
            print("Tela de carregamento finalizada.")
            return
        
        if not self.first_audio_played and self.sounds and self.sounds[0]:
            if current_time >= self.audio_start_time:
                pygame.mixer.stop() # Para qualquer som anterior (como o do menu, se ele não parou)
                self.sounds[0].play()
                self.first_audio_played = True # Marca que o primeiro áudio já foi tocado


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
            # Se for a primeira imagem, e o áudio dela já foi tocado pela lógica de atraso,
            # ou se não há som para essa imagem, não precisamos pará-lo ou tocá-lo novamente aqui.
            # Caso contrário, para o som anterior para tocar o novo.
            if self.current_image_index != -1: # Se não é a primeira atualização
                pygame.mixer.stop() # Para o som da imagem anterior

            self.current_image_index = target_index

            # Toca o som correspondente, se ele existir e se não for o primeiro áudio já tocado
            if self.current_image_index < len(self.sounds) and self.sounds[self.current_image_index]:
                if self.current_image_index == 0: # Se for a primeira imagem
                    if self.first_audio_played: # E o áudio dela JÁ foi tocado pelo atraso
                        # Não faz nada, pois o áudio já está tocando ou já terminou
                        pass
                    else:
                        # Isso não deveria acontecer se a lógica de atraso funcionar,
                        # mas é um fallback para garantir que não toque antes do atraso.
                        # Se chegar aqui para a imagem 0 e first_audio_played for False,
                        # significa que o atraso ainda não disparou, então não toque.
                        pass
                else: # Para qualquer outra imagem (índice > 0)
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
    

