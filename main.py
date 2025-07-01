# main.py
# Gerenciador de estados principal da aplicação.

import pygame
import os

# Imports relativos para funcionar com a execução de módulo (-m)
from .settings import (LARGURA_TELA, ALTURA_TELA, FPS, PASTA_AUDIO, 
                       AUDIO_LOADING_1, AUDIO_LOADING_2, AUDIO_EXPLICACAO_JOGO, AUDIO_MUSICA_FUNDO)
from .ui.menu import MainMenu
from .ui.screens import LoadingScreenToGame, EndScreen, GameBackground
from .game.main_game import game_loop 

def main():
    pygame.init()
    pygame.mixer.init() # Inicializa o mixer de áudio
    screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Oficina do Noel")
    clock = pygame.time.Clock()

    # --- Instâncias das Telas ---
    menu = MainMenu()
    
    # Prepara a tela de carregamento com as duas imagens e seus respectivos áudios
    loading_screen = LoadingScreenToGame(
        images=["loading1.png", "loading2.png"],
        durations=[3.0, 3.0], # Duração de cada imagem
        audio_path=[AUDIO_LOADING_1, AUDIO_LOADING_2] # Passa a lista de áudios
    )

    # Prepara as telas de fim de jogo e fundo
    end_screen = EndScreen()
    game_background = GameBackground()
    
    # Carrega o áudio de explicação
    path_explicacao = os.path.join(PASTA_AUDIO, AUDIO_EXPLICACAO_JOGO)
    sound_explicacao = None
    if os.path.exists(path_explicacao):
        sound_explicacao = pygame.mixer.Sound(path_explicacao)
    
    # Carrega a música de fundo do jogo
    path_musica_fundo = os.path.join(PASTA_AUDIO, AUDIO_MUSICA_FUNDO)

    # --- Máquina de Estados ---
    game_state = "MENU"
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
            
            elif game_state in ["GAME_OVER_VITORIA", "GAME_OVER_DERROTA"]:
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
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
                    if os.path.exists(path_musica_fundo):
                        pygame.mixer.music.load(path_musica_fundo)
                        pygame.mixer.music.play(-1)

        elif game_state == "EXPLAINING":
            game_background.draw(screen)
            # Verifica se o som de explicação terminou
            if not pygame.mixer.get_busy():
                game_state = "PLAYING"
                if os.path.exists(path_musica_fundo):
                    pygame.mixer.music.load(path_musica_fundo)
                    pygame.mixer.music.play(-1)

        elif game_state == "PLAYING":
            # Chama o loop do jogo e captura o resultado
            resultado = game_loop(screen, clock)
            pygame.mixer.music.stop()
            
            # Transiciona para o estado correto com base no resultado
            if resultado in ['VITORIA', 'DERROTA']:
                game_state = "GAME_OVER_" + resultado
            else: # Se saiu com ESC, o resultado é 'MENU'
                game_state = "MENU"

        elif game_state == "GAME_OVER_VITORIA":
            end_screen.draw(screen)
            # Aqui você pode adicionar um texto de "VITÓRIA!" sobre a tela

        elif game_state == "GAME_OVER_DERROTA":
            end_screen.draw(screen)
            # Aqui você pode adicionar um texto de "DERROTA!" sobre a tela

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()