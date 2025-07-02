# ui/menu.py
# Define a classe para a tela de menu principal.

from ..settings import FONTE_PATH, FONTE_BOLD_PATH, VERMELHO, VERMELHO, PRETO, BRANCO
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

        # --- TÍTULO ---
        title_text = self.font_title.render("Oficina do Noel", True, BRANCO)
        title_rect = title_text.get_rect(center=(screen.get_width() // 2, 80))
        title_box_rect = title_rect.inflate(20, 20)
        
        # 1. Desenha a caixa preta de fundo
        pygame.draw.rect(screen, PRETO, title_box_rect, border_radius=5)
        # 2. Desenha a borda por cima da caixa preta
        pygame.draw.rect(screen, VERMELHO, title_box_rect, width=3, border_radius=5)
        
        # Desenha o texto do título
        screen.blit(title_text, title_rect)

        # --- SUBTÍTULO 1 ---
        subtitle_text = self.font_subtitle.render("SSC0640 - Sistemas Operacionais I", True, BRANCO)
        subtitle_rect = subtitle_text.get_rect(center=(screen.get_width() // 2, 150))
        subtitle_box_rect = subtitle_rect.inflate(20, 20)
        
        # 1. Desenha a caixa preta
        pygame.draw.rect(screen, PRETO, subtitle_box_rect, border_radius=5)
        # 2. Desenha a borda
        pygame.draw.rect(screen, VERMELHO, subtitle_box_rect, width=3, border_radius=5)
        
        screen.blit(subtitle_text, subtitle_rect)

        # --- SUBTÍTULO 2 ---
        subtitle2_text = self.font_subtitle.render("Prof. Dr. Rodolfo I. Meneguette", True, BRANCO)
        subtitle2_rect = subtitle2_text.get_rect(center=(screen.get_width() // 2, 210)) 
        subtitle2_box_rect = subtitle2_rect.inflate(20, 20)
        
        # 1. Desenha a caixa preta
        pygame.draw.rect(screen, PRETO, subtitle2_box_rect, border_radius=5)
        # 2. Desenha a borda
        pygame.draw.rect(screen, VERMELHO, subtitle2_box_rect, width=3, border_radius=5)
        
        screen.blit(subtitle2_text, subtitle2_rect)


        # --- OPÇÕES DO MENU ---
        for i, option in enumerate(self.options):
            color = BRANCO if i == self.selected_option else VERMELHO
            option_text = self.font.render(option, True, color)
            option_rect = option_text.get_rect(center=(screen.get_width() // 2, 300 + i * 60)) 
            option_box_rect = option_rect.inflate(20, 20)
            
            # 1. Desenha a caixa preta de fundo
            pygame.draw.rect(screen, PRETO, option_box_rect, border_radius=5)

            # 2. Desenha a borda por cima
            # A cor da borda muda para BRANCO quando a opção está selecionada!
            cor_borda = BRANCO if i == self.selected_option else VERMELHO
            pygame.draw.rect(screen, cor_borda, option_box_rect, width=3, border_radius=5)

            # 3. Desenha o texto por cima de tudo
            screen.blit(option_text, option_rect)
