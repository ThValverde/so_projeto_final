# ui/screens.py
# Define as classes para as telas de carregamento e final.

from ..settings import LARGURA_TELA, ALTURA_TELA, PASTA_IMAGENS, FONTE_PATH, BRANCO, PRETO
import pygame   # Importa a biblioteca Pygame para manipulação de gráficos, som e eventos
import os   # Importa a biblioteca os para manipulação de caminhos de arquivos e diretórios

class MenuBackground:
    """Classe para o fundo do menu principal."""
    
    def __init__(self):
        self.image = pygame.image.load(os.path.join(PASTA_IMAGENS, "menubackground.png"))   # Carrega a imagem do fundo do menu
        self.image = pygame.transform.scale(self.image, (LARGURA_TELA, ALTURA_TELA))    # Redimensiona a imagem para o tamanho da tela
        self.rect = self.image.get_rect()   # Obtém o retângulo da imagem para posicionamento

    def draw(self, screen):
        """Desenha o fundo na tela."""
        screen.blit(self.image, self.rect)  # Desenha a imagem do fundo na tela usando o retângulo obtido
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
        self.durations = durations  # Durações em segundos para cada imagem
        
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
        self.current_image_index = -1   # Índice da imagem atual, começa em -1 para indicar que nenhuma imagem foi mostrada
        self.start_time = None  # Tempo em que a tela de carregamento foi iniciada
        self.finished = True # Começa como finalizado, só fica ativo após chamar start()
        
        self.initial_audio_delay = initial_audio_delay # Armazena o atraso desejado
        self.audio_start_time = 0 # Tempo em que o áudio deveria começar a tocar (start_time + delay)
        self.first_audio_played = False # Flag para garantir que o primeiro áudio só toque uma vez


    def start(self):    # Inicia a tela de carregamento, resetando o estado e preparando para mostrar as imagens
        print("Iniciando a tela de carregamento...")    # Mensagem de depuração para indicar que a tela de carregamento foi iniciada
        self.start_time = pygame.time.get_ticks()   # Obtém o tempo atual em milissegundos desde que o Pygame foi iniciado
        self.current_image_index = -1   # Reseta o índice da imagem atual para -1, indicando que nenhuma imagem foi mostrada ainda
        self.finished = False   # Marca a tela como não finalizada, permitindo que o update e draw funcionem
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
        target_index = 0    # Começa com o índice 0, que é a primeira imagem
        cumulative_time = 0 # Acumulador para calcular o tempo total decorrido
        for i, duration in enumerate(self.durations):   # Itera sobre as durações para encontrar a imagem correta
            cumulative_time += duration # Soma a duração da imagem atual ao acumulador
            if elapsed_time < cumulative_time:  # Se o tempo decorrido é menor que o tempo acumulado    
                target_index = i    # Define o índice da imagem atual como o índice da iteração
                break   # Sai do loop, pois já encontrou a imagem correta

        # Se o índice da imagem mudou, toca o novo som
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
                        pass
                else: # Para qualquer outra imagem (índice > 0)
                    self.sounds[self.current_image_index].play()
                    
    def draw(self, screen):
        if not self.finished and self.images and self.current_image_index != -1:
            current_image = self.images[self.current_image_index]
            screen.blit(current_image, (0, 0))
            try:
                from ..settings import FONTE_PATH, BRANCO
                font_pular = pygame.font.Font(FONTE_PATH, 18)
                texto_pular = font_pular.render("Pressione ESPAÇO para pular", True, BRANCO)
                # Posiciona no canto inferior direito
                pos_x = LARGURA_TELA - texto_pular.get_width() - 20
                pos_y = ALTURA_TELA - texto_pular.get_height() - 20
                screen.blit(texto_pular, (pos_x, pos_y))
            except:
                pass # Se falhar, simplesmente não desenha o texto

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
    


class ReadmeScreen:
    """
    Uma tela que exibe o conteúdo de um arquivo de texto com funcionalidade de rolagem.
    """
    def __init__(self, filepath, font_size=18, line_height=22):
        """
        Inicializa a tela do Readme.
        Args:
            filepath (str): Caminho para o arquivo .txt a ser lido.
            font_size (int): Tamanho da fonte para o texto.
            line_height (int): Espaçamento vertical entre as linhas.
        """
        self.font = pygame.font.Font(FONTE_PATH, font_size) # Carrega a fonte do arquivo especificado
        self.line_height = line_height  # Define a altura de cada linha de texto
        self.lines_surfaces = []    # Lista para armazenar as superfícies de texto renderizadas
        self.scroll_y = 0  # Deslocamento vertical atual da rolagem
        self.total_height = 0   # Altura total do texto, usada para limitar a rolagem
        # Carrega e renderiza cada linha do arquivo de texto
        try:   
            with open(filepath, 'r', encoding='utf-8') as f:    # Abre o arquivo de texto para leitura
                lines = f.readlines()   # Lê todas as linhas do arquivo
                for line in lines:  # Itera sobre cada linha
                    line_surface = self.font.render(line.strip(), True, BRANCO) # Renderiza a linha como uma superfície de texto
                    self.lines_surfaces.append(line_surface)    # Adiciona a superfície renderizada à lista de superfícies
            self.total_height = len(self.lines_surfaces) * self.line_height # Calcula a altura total do texto baseado no número de linhas e na altura de cada linha
        except FileNotFoundError:   # Tenta abrir o arquivo, mas captura o erro se não for encontrado
            print(f"AVISO: Arquivo do Readme não encontrado em {filepath}") # Exibe um aviso no console se o arquivo não for encontrado
            error_msg = "Arquivo README.txt não encontrado na raiz do projeto!" 
            error_surface = self.font.render(error_msg, True, (255, 100, 100))  # Renderiza uma mensagem de erro em vermelho
            self.lines_surfaces.append(error_surface)   # Adiciona uma mensagem de erro à lista de superfícies
            self.total_height = self.line_height    # Define a altura total como a altura de uma linha, pois só há uma mensagem de erro

    def handle_event(self, event):
        """Processa eventos de input para rolagem."""
        scroll_speed = self.line_height * 3 # Rola 3 linhas por vez

        if event.type == pygame.KEYDOWN:    # Verifica se uma tecla foi pressionada
            if event.key == pygame.K_UP:    # Se a tecla pressionada for a seta para cima
                self.scroll_y -= scroll_speed   # Rola para cima
            elif event.key == pygame.K_DOWN:    # Se a tecla pressionada for a seta para baixo
                self.scroll_y += scroll_speed   # Rola para baixo
        elif event.type == pygame.MOUSEWHEEL:   # Verifica se a roda do mouse foi rolada
            self.scroll_y -= event.y * scroll_speed # Rola para cima ou para baixo baseado na direção da roda do mouse
        # Limita a rolagem para não sair do texto
        self.scroll_y = max(0, self.scroll_y) # Limite superior (não rolar acima do início)
        max_scroll = self.total_height - ALTURA_TELA + 100 # Limite inferior
        self.scroll_y = min(max_scroll, self.scroll_y) if max_scroll > 0 else 0
    def draw(self, screen):
        """Desenha o texto rolável na tela."""
        screen.fill(PRETO)  # Limpa a tela com a cor preta
        y_pos = 50 # Margem superior inicial
        for line_surface in self.lines_surfaces:
            # Posição de desenho é ajustada pela rolagem atual
            draw_pos_y = y_pos - self.scroll_y
            # Verifica se a linha está dentro da área visível da tela
            if draw_pos_y > -self.line_height and draw_pos_y < ALTURA_TELA:
                screen.blit(line_surface, (50, draw_pos_y)) # Margem esquerda de 50px
            y_pos += self.line_height
        # Instrução fixa de como navegar e sair
        instrucao_font = pygame.font.Font(FONTE_PATH, 16)
        instrucao_text = instrucao_font.render("Use as SETAS ou o SCROLL do mouse para navegar | Pressione ESC para voltar", True, (150, 150, 150))
        screen.blit(instrucao_text, (20, ALTURA_TELA - 30))