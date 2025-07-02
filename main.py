# main.py
# Ponto de entrada da aplicação. Gerencia a máquina de estados principal do jogo,
# controlando o fluxo entre Menu, Telas de Carregamento, Jogo e Telas de Fim de Jogo.
# Também é responsável por criar e destruir a instância de 'GameMechanics'.

import pygame   # Importa a biblioteca Pygame para manipulação de gráficos, som e eventos
import os   # Importa a biblioteca os para manipulação de caminhos de arquivos e diretórios

from .settings import (LARGURA_TELA, ALTURA_TELA, FPS, PASTA_AUDIO, AUDIO_START,
                       AUDIO_LOADING_1, AUDIO_LOADING_2, AUDIO_LOADING_3, AUDIO_LOADING_4,
                       AUDIO_EXPLICACAO_JOGO, AUDIO_MUSICA_FUNDO,
                       FONTE_BOLD_PATH, FONTE_PATH, BRANCO, VERMELHO)
from .ui.menu import MainMenu
from .ui.screens import LoadingScreenToGame, EndScreen, GameBackground
from .game.main_game import game_loop   # Importa a função game_loop do módulo main_game, que contém a lógica principal do jogo
from .game.mechanics import GameMechanics

def main(): 
    pygame.init() # Inicializa todos os módulos do Pygame
    pygame.mixer.init() # Inicializa o mixer de som do Pygame
    screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))   # Cria a janela do jogo com as dimensões especificadas
    pygame.display.set_caption("Oficina do Noel")   # Define o título da janela do jogo
    clock = pygame.time.Clock() # Cria um objeto Clock para controlar a taxa de quadros do jogo

    # --- Instâncias das Telas ---
    menu = MainMenu()
    loading_screen = LoadingScreenToGame(
        images=["loading1.png", "loading2.png", "loading2.png", "loading3.png"],
        durations=[13.0, 18.0, 39.8, 88.9],
        # durations = [1,1,1,1],
        audio_path=[AUDIO_LOADING_1, AUDIO_LOADING_2, AUDIO_LOADING_3, AUDIO_LOADING_4],
        initial_audio_delay=1.5
    )
    end_screen = EndScreen()    # Cria uma instância da tela de fim de jogo
    game_background = GameBackground()  # Cria uma instância do fundo do jogo
    
    # --- Carregamento de Recursos ---  
    font_fim_titulo = pygame.font.Font(FONTE_BOLD_PATH, 60)     # Fonte para o título da tela de fim de jogo
    font_fim_instrucao = pygame.font.Font(FONTE_PATH, 28)   # Fonte para as instruções da tela de fim de jogo
    
    path_explicacao = os.path.join(PASTA_AUDIO, AUDIO_EXPLICACAO_JOGO)  # Caminho para o áudio de explicação do jogo    
    sound_explicacao = None # Inicializa a variável de som de explicação como None
    if os.path.exists(path_explicacao): # Verifica se o arquivo de áudio de explicação existe
        sound_explicacao = pygame.mixer.Sound(path_explicacao)  # Carrega o áudio de explicação do jogo
    
    path_musica_fundo = os.path.join(PASTA_AUDIO, AUDIO_MUSICA_FUNDO)
    if os.path.exists(path_musica_fundo):   # Verifica se o arquivo de música de fundo existe
        pygame.mixer.music.load(path_musica_fundo)  # Carrega a música de fundo
        pygame.mixer.music.play(-1) # Reproduz a música de fundo em loop
        pygame.mixer.music.set_volume(0.25) # Define o volume da música de fundo
    else:
        print(f"AVISO: Música de fundo não encontrada em {path_musica_fundo}")

    path_intro_audio = os.path.join(PASTA_AUDIO, AUDIO_START)
    if os.path.exists(path_intro_audio):
        intro_sound = pygame.mixer.Sound(path_intro_audio)
        intro_sound.play() # Toca uma única vez
    else:
        print(f"AVISO: Áudio de introdução não encontrado em {path_intro_audio}")


    # --- Máquina de Estados ---
    game_state = "MENU"
    game_mechanics_instance = None 
    running = True
    is_muted = False

    # --- Máquina de Estados ---    
    game_state = "MENU" # Estado inicial do jogo, começa no menu principal
    game_mechanics_instance = None  # Inicializa a instância de GameMechanics como None, será criada quando o jogo for iniciado
    running = True  # Variável de controle do loop principal do jogo
    is_muted = False    # Variável para controlar o estado de mudo do jogo

    while running:  
        events = pygame.event.get() # Obtém todos os eventos da fila de eventos do Pygame
        for event in events:            
            if event.type == pygame.QUIT:   # Verifica se o evento é de fechamento da janela
                running = False   # Se for, encerra o loop principal do jogo
            
            # --- Lógica de Eventos por Estado ---
            if event.type == pygame.KEYDOWN:    
                if event.key == pygame.K_m: # Alterna o estado de mudo do jogo
                    is_muted = not is_muted
                    if is_muted: pygame.mixer.music.pause()
                    else: pygame.mixer.music.unpause()
                elif event.key == pygame.K_v:   # Aumenta o volume da música de fundo
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
                            if intro_sound and intro_sound.get_num_channels() > 0:
                                intro_sound.stop()
                                
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

        if game_state == "MENU":    # Desenha o menu principal
            menu.draw(screen)
        
        elif game_state == "LOADING":   # Desenha a tela de carregamento
            loading_screen.update()
            loading_screen.draw(screen)
            if loading_screen.finished:
                game_state = "EXPLAINING"   # Muda para o estado de explicação após o carregamento
                if sound_explicacao:
                    sound_explicacao.play() # Reproduz o áudio de explicação do jogo

        elif game_state == "EXPLAINING":    # Desenha a tela de explicação do jogo
            game_background.draw(screen)
            if not pygame.mixer.get_busy(): # Verifica se o áudio de explicação terminou
                game_state = "PLAYING"  # Muda para o estado de jogo após a explicação
                if game_mechanics_instance:
                    game_mechanics_instance.iniciar_sistema()

        elif game_state == "PLAYING":   # Executa o loop principal do jogo
            resultado = game_loop(screen, clock, game_mechanics_instance)
            
            if game_mechanics_instance: # Se a instância de GameMechanics existir, para o sistema
                game_mechanics_instance.parar_sistema() #   Para o sistema de mecânicas do jogo
            
            if resultado in ['VITORIA', 'DERROTA']: # Se o resultado do jogo for vitória ou derrota, muda o estado do jogo
                game_state = "GAME_OVER_" + resultado   #   Concatena o resultado para definir o estado de fim de jogo
            else:
                game_state = "MENU"   # Se o resultado não for vitória ou derrota, volta para o menu principal

        elif game_state == "GAME_OVER_VITORIA": # Desenha a tela de fim de jogo para vitória
            end_screen.draw(screen)
            texto_titulo = font_fim_titulo.render("VITÓRIA!", True, BRANCO)
            texto_instrucao = font_fim_instrucao.render("Pressione ENTER para jogar de novo ou ESC para o menu", True, BRANCO)
            screen.blit(texto_titulo, texto_titulo.get_rect(center=(LARGURA_TELA/2, ALTURA_TELA/2 - 50)))
            screen.blit(texto_instrucao, texto_instrucao.get_rect(center=(LARGURA_TELA/2, ALTURA_TELA/2 + 50)))

        elif game_state == "GAME_OVER_DERROTA": # Desenha a tela de fim de jogo para derrota
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