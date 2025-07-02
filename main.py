# main.py
# Gerenciador de estados principal da aplicação.

import pygame
import os

# Imports relativos para funcionar com a execução de módulo (-m)
from .settings import (LARGURA_TELA, ALTURA_TELA, FPS, PASTA_AUDIO, 
                       AUDIO_LOADING_1, AUDIO_LOADING_2, AUDIO_LOADING_3, 
                       AUDIO_EXPLICACAO_JOGO, AUDIO_MUSICA_FUNDO,
                       FONTE_BOLD_PATH, FONTE_PATH, BRANCO, VERMELHO) # Adicionado fontes e cores
from .ui.menu import MainMenu
from .ui.screens import LoadingScreenToGame, EndScreen, GameBackground
from .game.main_game import game_loop 
from .game.mechanics import GameMechanics

def main():
    pygame.init()
    pygame.mixer.init() # Inicializa o mixer de áudio
    screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Oficina do Noel")
    clock = pygame.time.Clock()

    # --- Instâncias das Telas e Mecânicas ---
    menu = MainMenu()
    
    loading_screen = LoadingScreenToGame(
        images=["loading1.png", "loading2.png", "loading3.png"],
        durations=[3.0, 3.0, 3.0],
        audio_path=[AUDIO_LOADING_1, AUDIO_LOADING_2, AUDIO_LOADING_3]
    )

    end_screen = EndScreen()
    game_background = GameBackground()
    game_mechanics = GameMechanics()
    
    # --- Carregamento de Recursos ---
    # Fontes para as telas de fim de jogo
    font_fim_titulo = pygame.font.Font(FONTE_BOLD_PATH, 60)
    font_fim_instrucao = pygame.font.Font(FONTE_PATH, 28)

    # Áudio de explicação
    path_explicacao = os.path.join(PASTA_AUDIO, AUDIO_EXPLICACAO_JOGO)
    sound_explicacao = None
    if os.path.exists(path_explicacao):
        sound_explicacao = pygame.mixer.Sound(path_explicacao)
    
    # Música de fundo
    path_musica_fundo = os.path.join(PASTA_AUDIO, AUDIO_MUSICA_FUNDO)

    # --- Máquina de Estados ---
    game_state = "MENU"
    sistema_iniciado = False
    running = True

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            
            # --- Lógica de Eventos por Estado ---
            if game_state == "MENU":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        menu.selected_option = (menu.selected_option - 1) % len(menu.options)
                    elif event.key == pygame.K_DOWN:
                        menu.selected_option = (menu.selected_option + 1) % len(menu.options)
                    elif event.key == pygame.K_RETURN:
                        if menu.options[menu.selected_option] == "Iniciar Jogo":
                            game_state = "LOADING"
                            loading_screen.start()
                        elif menu.options[menu.selected_option] == "Sair":
                            running = False
            
            # (LÓGICA DE REINÍCIO IMPLEMENTADA AQUI)
            elif game_state in ["GAME_OVER_VITORIA", "GAME_OVER_DERROTA"]:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN: # ENTER para jogar de novo
                        game_state = "LOADING"
                        loading_screen.start()
                    elif event.key == pygame.K_ESCAPE: # ESC para voltar ao menu
                        game_state = "MENU"

        # --- Lógica de Atualização e Renderização por Estado ---
        screen.fill((0, 0, 0))

        if game_state == "MENU":
            menu.draw(screen)
        
        elif game_state == "LOADING":
            loading_screen.update()
            loading_screen.draw(screen)
            if loading_screen.finished:
                game_state = "EXPLAINING"
                if sound_explicacao:
                    sound_explicacao.play()
                else:
                    print("AVISO: Áudio de explicação não encontrado. Pulando para o jogo...")
                    game_state = "PLAYING"
                    if not sistema_iniciado:
                        game_mechanics.iniciar_sistema()
                        sistema_iniciado = True
                    if os.path.exists(path_musica_fundo):
                        pygame.mixer.music.load(path_musica_fundo)
                        pygame.mixer.music.play(-1)

        elif game_state == "EXPLAINING":
            game_background.draw(screen)
            if not pygame.mixer.get_busy():
                game_state = "PLAYING"
                if not sistema_iniciado:
                    game_mechanics.iniciar_sistema()
                    sistema_iniciado = True
                if os.path.exists(path_musica_fundo):
                    pygame.mixer.music.load(path_musica_fundo)
                    pygame.mixer.music.play(-1)

        elif game_state == "PLAYING":
            resultado = game_loop(screen, clock, game_mechanics)
            pygame.mixer.music.stop()
            
            if resultado in ['VITORIA', 'DERROTA']:
                game_mechanics.reiniciar_estado_jogo() 
                game_state = "GAME_OVER_" + resultado
            else:
                game_state = "MENU"

        elif game_state == "GAME_OVER_VITORIA":
            end_screen.draw(screen)
            # Renderiza o texto de vitória e instruções
            texto_titulo = font_fim_titulo.render("VITÓRIA!", True, BRANCO)
            texto_instrucao = font_fim_instrucao.render("Pressione ENTER para jogar de novo ou ESC para o menu", True, BRANCO)
            screen.blit(texto_titulo, texto_titulo.get_rect(center=(LARGURA_TELA/2, ALTURA_TELA/2 - 50)))
            screen.blit(texto_instrucao, texto_instrucao.get_rect(center=(LARGURA_TELA/2, ALTURA_TELA/2 + 50)))

        elif game_state == "GAME_OVER_DERROTA":
            end_screen.draw(screen)
            # Renderiza o texto de derrota e instruções
            texto_titulo = font_fim_titulo.render("FIM DE JOGO", True, VERMELHO)
            texto_instrucao = font_fim_instrucao.render("Pressione ENTER para jogar de novo ou ESC para o menu", True, BRANCO)
            screen.blit(texto_titulo, texto_titulo.get_rect(center=(LARGURA_TELA/2, ALTURA_TELA/2 - 50)))
            screen.blit(texto_instrucao, texto_instrucao.get_rect(center=(LARGURA_TELA/2, ALTURA_TELA/2 + 50)))

        pygame.display.flip()
        clock.tick(FPS)

    # Garante que as threads sejam paradas ao sair do jogo
    game_mechanics.parar_sistema()
    pygame.quit()