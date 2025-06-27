# game/main_game.py
# Contém a lógica principal do gameplay (versão para teste visual da MesaDePresentes).

import pygame
import sys

# Importa as classes e configurações necessárias
from ..settings import LARGURA_TELA, ALTURA_TELA, FPS
from ..ui.screens import GameBackground
# (MODIFICADO) Importa apenas as entidades visuais que vamos usar
from .entities import Esteira, Elfo, MesaDePresentes
# from ..mechanics import Gerenciador Da Mesa DePresentes # (REMOVIDO) Não precisamos do gerenciador para este teste

def game_loop(screen, clock):
    """
    Função que contém o loop principal do jogo para testar a parte VISUAL da MesaDePresentes.

    Args:
        screen (pygame.Surface): A superfície principal da tela do jogo.
        clock (pygame.time.Clock): O objeto de relógio do Pygame para controlar o FPS.
    """
    # --- Configuração dos Elementos do Jogo ---
    background = GameBackground()
    all_sprites = pygame.sprite.Group()

    # --- Configuração das Esteiras ---
    # (O código das esteiras continua o mesmo)
    y_pos_esteiras = (ALTURA_TELA / 2) - 80
    espacamento_horizontal_esteiras = 180
    largura_esteira = 200
    altura_esteira = 60
    x_pos_inicial_esteiras = (-60 + (LARGURA_TELA - (2 * espacamento_horizontal_esteiras) - largura_esteira) / 2)
    esteira1 = Esteira(position=(x_pos_inicial_esteiras, y_pos_esteiras), size=(largura_esteira, altura_esteira))
    esteira2 = Esteira(position=(x_pos_inicial_esteiras + espacamento_horizontal_esteiras, y_pos_esteiras), size=(largura_esteira, altura_esteira))
    esteira3 = Esteira(position=(x_pos_inicial_esteiras + espacamento_horizontal_esteiras * 2, y_pos_esteiras), size=(largura_esteira, altura_esteira))
    all_sprites.add(esteira1, esteira2, esteira3)

    # --- Configuração da MesaDePresentes (Apenas a parte visual) ---
    MesaDePresentes_sprite = MesaDePresentes(position=(x_pos_inicial_esteiras + espacamento_horizontal_esteiras*3 + 30, ALTURA_TELA * 0.8))
    all_sprites.add(MesaDePresentes_sprite)

    # --- Configuração do Elfo ---
    y_pos_elfo = ALTURA_TELA * 0.85
    POSICOES_ELFO = [
        (esteira1.rect.centerx, y_pos_elfo),
        (esteira2.rect.centerx, y_pos_elfo),
        (esteira3.rect.centerx, y_pos_elfo),
        (MesaDePresentes_sprite.rect.centerx, y_pos_elfo)
    ]
    player = Elfo(positions=POSICOES_ELFO, start_index=0)
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
                    running = False
                
                # Controle do Elfo
                if event.key == pygame.K_a:
                    player.move("left")
                elif event.key == pygame.K_d:
                    player.move("right")
                
                # --- (LÓGICA DE TESTE VISUAL) ---
                # Se pressionar ESPAÇO e o Elfo estiver na posição da MesaDePresentes...
                elif event.key == pygame.K_SPACE:
                    if player.position_index == 3: # Índice da posição da MesaDePresentes
                        print("Tecla ESPAÇO: Testando adicionar visual de presente...")
                        # Chama o método diretamente na entidade visual
                        MesaDePresentes_sprite.adicionar_presente_visual()
                
                # (NOVO) Se pressionar 'R', remove um presente visual para teste
                elif event.key == pygame.K_r:
                    print("Tecla R: Testando remover visual de presente...")
                    # Chama o método diretamente na entidade visual
                    MesaDePresentes_sprite.remover_presente_visual()

        # --- Lógica de Atualização ---
        all_sprites.update()

        # --- Lógica de Desenho ---
        background.draw(screen)
        all_sprites.draw(screen)
        pygame.display.flip()
        
        # --- Controle de FPS ---
        clock.tick(FPS)