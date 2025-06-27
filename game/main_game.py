# game/main_game.py
# Contém a lógica principal e o loop do gameplay.

import pygame
import sys

# Importa as classes e configurações necessárias
from ..settings import LARGURA_TELA, ALTURA_TELA, FPS
from ..ui.screens import GameBackground
from .entities import Esteira, Elfo # Importa ambas as entidades

def game_loop(screen, clock):
    """
    Função que contém o loop principal do jogo, com esteiras e o jogador.

    Args:
        screen (pygame.Surface): A superfície principal da tela do jogo.
        clock (pygame.time.Clock): O objeto de relógio do Pygame para controlar o FPS.
    """
    # --- Configuração dos Elementos do Jogo ---
    background = GameBackground()
    all_sprites = pygame.sprite.Group()

    # --- Configuração das Esteiras (com posicionamento horizontal) ---
    y_pos_esteiras = (ALTURA_TELA / 2) - 80 # Posição Y, um pouco acima do centro
    espacamento_horizontal = 160
    largura_esteira = 200  # (NOVO) Define a largura como uma variável para reutilizar
    altura_esteira = 60

    # Posição X da primeira esteira para centralizar o conjunto
    x_pos_inicial = 100

    esteira1 = Esteira(position=(x_pos_inicial, y_pos_esteiras), size=(largura_esteira, altura_esteira))
    esteira2 = Esteira(position=(x_pos_inicial + espacamento_horizontal, y_pos_esteiras), size=(largura_esteira, altura_esteira))
    esteira3 = Esteira(position=(x_pos_inicial + espacamento_horizontal * 2, y_pos_esteiras), size=(largura_esteira, altura_esteira))
    all_sprites.add(esteira1, esteira2, esteira3)

    # --- Configuração do Elfo (Jogador) ---
    # A posição Y do Elfo, mais para baixo na tela
    y_pos_elfo = ALTURA_TELA * 0.85

    # (MODIFICADO) As posições X do Elfo agora são calculadas a partir do centro das esteiras
    POSICOES_ELFO = [
        (esteira1.rect.centerx, y_pos_elfo), # Posição abaixo do centro da esteira 1
        (esteira2.rect.centerx, y_pos_elfo), # Posição abaixo do centro da esteira 2
        (esteira3.rect.centerx, y_pos_elfo)  # Posição abaixo do centro da esteira 3
    ]
    # O código original tinha 4 posições para o Elfo, mas apenas 3 esteiras.
    # Ajustei para 3 posições para um alinhamento direto.
    
    player = Elfo(positions=POSICOES_ELFO, start_index=1)
    all_sprites.add(player)

    # --- Loop Principal do Jogo ---
    running = True
    while running:
        # --- Processamento de Eventos ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False # Sai do loop do jogo para voltar ao menu
                
                # Controle do Elfo
                if event.key == pygame.K_a:
                    player.move("left")
                elif event.key == pygame.K_d:
                    player.move("right")

        # --- Lógica de Atualização ---
        all_sprites.update()

        # --- Lógica de Desenho ---
        background.draw(screen)
        all_sprites.draw(screen)
        pygame.display.flip()
        
        # --- Controle de FPS ---
        clock.tick(FPS)