# ui/menu.py
# Define a classe para a tela de menu principal.

from ..settings import FONTE_PATH, FONTE_BOLD_PATH, VERDE_ESCURO, VERDE_CLARO, PRETO, AMARELO
from .screens import EndScreen
from .screens import MenuBackground  
import pygame

class MainMenu:
    """Classe para o menu principal do jogo."""

    def __init__(self):
        self.background = MenuBackground()
        self.font_title = pygame.font.Font(FONTE_BOLD_PATH, 60)
        self.font_subtitle = pygame.font.Font(FONTE_BOLD_PATH, 30)
        self.font = pygame.font.Font(FONTE_PATH, 30)
        self.options = ["Iniciar Jogo", "Readme" ,"Sair"]
        self.selected_option = 0

    def draw(self, screen):
        """Desenha o menu na tela."""
        self.background.draw(screen)
        title_text = self.font_title.render("Jogo Nome", True, AMARELO)
        title_rect = title_text.get_rect(center=(screen.get_width() // 2, 100))
        # Crie o retângulo de fundo um pouco maior que o texto
        title_box_rect = title_rect.inflate(20, 20) # Adiciona 20px de padding horizontal e vertical
        pygame.draw.rect(screen, PRETO, title_box_rect, border_radius=5) # Desenha a caixa preta
        
        # Desenha o subtítulo 1
        subtitle_text = self.font_subtitle.render("SSC0640 - Sistemas Operacionais I", True, AMARELO)
        subtitle_rect = subtitle_text.get_rect(center=(screen.get_width() // 2, 150))
        # Cria o retângulo de fundo para o subtítulo, um pouco maior que o texto
        subtitle_box_rect = subtitle_rect.inflate(20, 20) # Adiciona padding
        pygame.draw.rect(screen, PRETO, subtitle_box_rect, border_radius=5)
        screen.blit(subtitle_text, subtitle_rect)

        # Desenha o subtítulo 2
        subtitle2_text = self.font_subtitle.render("Prof. Dr. Rodolfo I. Meneguette", True, AMARELO)
        subtitle2_rect = subtitle2_text.get_rect(center=(screen.get_width() // 2, 200)) 
        # Cria o retângulo de fundo para o segundo subtítulo, um pouco maior que o texto
        subtitle2_box_rect = subtitle2_rect.inflate(20, 20) # Adiciona padding
        pygame.draw.rect(screen, PRETO, subtitle2_box_rect, border_radius=5)
        screen.blit(subtitle2_text, subtitle2_rect)

        # Desenha o texto por cima da caixa
        screen.blit(title_text, title_rect)
        for i, option in enumerate(self.options):
            color = AMARELO if i == self.selected_option else VERDE_ESCURO
            option_text = self.font.render(option, True, color)
            option_rect = option_text.get_rect(center=(screen.get_width() // 2, 300 + i * 100)) 

            # Cria o retângulo de fundo para a opção, um pouco maior que o texto
            option_box_rect = option_rect.inflate(20, 20) # Adiciona padding

            # 3. Desenha a caixa de fundo PRETA na tela ANTES do texto
            pygame.draw.rect(screen, PRETO, option_box_rect, border_radius=5)

            screen.blit(option_text, option_rect)

