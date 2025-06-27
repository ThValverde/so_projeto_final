# main.py
# Gerenciador de estados principal da aplicação.

import pygame

# Imports relativos para funcionar com a execução de módulo (-m)
from .settings import LARGURA_TELA, ALTURA_TELA, FPS
from .ui.menu import MainMenu
from .ui.screens import LoadingScreenToGame
from .game.main_game import game_loop 

def main():
    pygame.init()
    screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Oficina do Noel")
    
    clock = pygame.time.Clock()

    # --- Instanciação dos Módulos de Tela ---
    menu = MainMenu()
    
    # Configuração da tela de carregamento para o teste
    loading_images = ["loading1.png", "loading2.png"] # Use suas imagens
    loading_durations = [1.0, 1.0] # Durações para o teste
    loading_screen = LoadingScreenToGame(loading_images, loading_durations, audio_path=None)

    # --- Máquina de Estados ---
    game_state = "MENU"
    running = True

    while running:
        # --- Loop de Eventos ---
        # Este loop captura eventos globais como fechar a janela ou eventos do menu
        # Eventos específicos do jogo (como mover o elfo) são tratados dentro do game_loop
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            
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

        # --- Lógica de Desenho e Atualização por Estado ---
        screen.fill((0, 0, 0))

        if game_state == "MENU":
            menu.draw(screen)
        
        elif game_state == "LOADING":
            loading_screen.update()
            loading_screen.draw(screen)
            if loading_screen.finished:
                game_state = "PLAYING"

        elif game_state == "PLAYING":
            # Chama a função que contém o loop do gameplay
            game_loop(screen, clock)
            # Ao sair do game_loop (pressionando ESC), retorna ao menu
            game_state = "MENU"

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()