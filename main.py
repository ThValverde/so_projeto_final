# main.py
# Gerenciador de estados principal da aplicação.

import pygame
import os

from .settings import (LARGURA_TELA, ALTURA_TELA, FPS, PASTA_AUDIO, 
                       AUDIO_LOADING_1, AUDIO_LOADING_2, AUDIO_LOADING_3, 
                       AUDIO_EXPLICACAO_JOGO, AUDIO_MUSICA_FUNDO,
                       FONTE_BOLD_PATH, FONTE_PATH, BRANCO, VERMELHO)
from .ui.menu import MainMenu
from .ui.screens import LoadingScreenToGame, EndScreen, GameBackground
from .game.main_game import game_loop 
from .game.mechanics import GameMechanics

def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Oficina do Noel")
    clock = pygame.time.Clock()

    # --- Instâncias das Telas ---
    menu = MainMenu()
    loading_screen = LoadingScreenToGame(
        images=["loading1.png", "loading2.png", "loading3.png"],
        durations=[3.0, 3.0, 3.0],
        audio_path=[AUDIO_LOADING_1, AUDIO_LOADING_2, AUDIO_LOADING_3]
    )
    end_screen = EndScreen()
    game_background = GameBackground()
    
    # --- Carregamento de Recursos ---
    font_fim_titulo = pygame.font.Font(FONTE_BOLD_PATH, 60)
    font_fim_instrucao = pygame.font.Font(FONTE_PATH, 28)
    
    path_explicacao = os.path.join(PASTA_AUDIO, AUDIO_EXPLICACAO_JOGO)
    sound_explicacao = None
    if os.path.exists(path_explicacao):
        sound_explicacao = pygame.mixer.Sound(path_explicacao)
    
    path_musica_fundo = os.path.join(PASTA_AUDIO, AUDIO_MUSICA_FUNDO)
    if os.path.exists(path_musica_fundo):
        pygame.mixer.music.load(path_musica_fundo)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.25)
    else:
        print(f"AVISO: Música de fundo não encontrada em {path_musica_fundo}")

    # --- Máquina de Estados ---
    game_state = "MENU"
    game_mechanics_instance = None 
    running = True
    is_muted = False

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            
            # --- Lógica de Eventos por Estado ---
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    is_muted = not is_muted
                    if is_muted: pygame.mixer.music.pause()
                    else: pygame.mixer.music.unpause()
                elif event.key == pygame.K_v:
                    current_volume = pygame.mixer.music.get_volume()
                    new_volume = current_volume + 0.25
                    if new_volume > 1.0: new_volume = 0.25
                    pygame.mixer.music.set_volume(new_volume)

            if game_state == "MENU":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        menu.selected_option = (menu.selected_option - 1) % len(menu.options)
                    elif event.key == pygame.K_DOWN:
                        menu.selected_option = (menu.selected_option + 1) % len(menu.options)
                    elif event.key == pygame.K_RETURN:
                        selected_text = menu.options[menu.selected_option]
                        if selected_text == "Iniciar Jogo":
                            game_mechanics_instance = GameMechanics()
                            game_state = "LOADING"
                            loading_screen.start()
                        elif selected_text == "Readme":
                            print("Lógica para a tela 'Readme' a ser implementada.")
                        elif selected_text == "Sair":
                            running = False
            
            elif game_state in ["GAME_OVER_VITORIA", "GAME_OVER_DERROTA"]:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_mechanics_instance = GameMechanics()
                        game_state = "LOADING"
                        loading_screen.start()
                    elif event.key == pygame.K_ESCAPE:
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

        elif game_state == "EXPLAINING":
            game_background.draw(screen)
            if not pygame.mixer.get_busy():
                game_state = "PLAYING"
                if game_mechanics_instance:
                    game_mechanics_instance.iniciar_sistema()

        elif game_state == "PLAYING":
            resultado = game_loop(screen, clock, game_mechanics_instance)
            
            if game_mechanics_instance:
                game_mechanics_instance.parar_sistema()
            
            if resultado in ['VITORIA', 'DERROTA']:
                game_state = "GAME_OVER_" + resultado
            else:
                game_state = "MENU"

        # --- (BLOCO DE CÓDIGO CORRIGIDO/ADICIONADO) ---
        elif game_state == "GAME_OVER_VITORIA":
            end_screen.draw(screen)
            texto_titulo = font_fim_titulo.render("VITÓRIA!", True, BRANCO)
            texto_instrucao = font_fim_instrucao.render("Pressione ENTER para jogar de novo ou ESC para o menu", True, BRANCO)
            screen.blit(texto_titulo, texto_titulo.get_rect(center=(LARGURA_TELA/2, ALTURA_TELA/2 - 50)))
            screen.blit(texto_instrucao, texto_instrucao.get_rect(center=(LARGURA_TELA/2, ALTURA_TELA/2 + 50)))

        elif game_state == "GAME_OVER_DERROTA":
            end_screen.draw(screen)
            texto_titulo = font_fim_titulo.render("FIM DE JOGO", True, VERMELHO)
            texto_instrucao = font_fim_instrucao.render("Pressione ENTER para jogar de novo ou ESC para o menu", True, BRANCO)
            screen.blit(texto_titulo, texto_titulo.get_rect(center=(LARGURA_TELA/2, ALTURA_TELA/2 - 50)))
            screen.blit(texto_instrucao, texto_instrucao.get_rect(center=(LARGURA_TELA/2, ALTURA_TELA/2 + 50)))


        # Lógica de Mudo (desenha por cima de tudo)
        if is_muted:
            texto_mudo = font_fim_instrucao.render("Mudo (M)", True, BRANCO)
            pos_x = LARGURA_TELA - texto_mudo.get_width() - 10
            pos_y = ALTURA_TELA - texto_mudo.get_height() - 10
            screen.blit(texto_mudo, (pos_x, pos_y))


        pygame.display.flip()
        clock.tick(FPS)

    if game_mechanics_instance:
        game_mechanics_instance.parar_sistema()
    pygame.quit()