# main.py

# Imports que você já corrigiu
from .settings import LARGURA_TELA, ALTURA_TELA, FPS
from .ui.menu import MainMenu
import pygame

# Teste do menu principal
def main():
    # O import do pygame aqui dentro é redundante, mas não tem problema.
    # Pode deixar ou remover.
    import pygame 
    from .settings import LARGURA_TELA, ALTURA_TELA, FPS

    pygame.init()
    screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Menu Principal")
    
    clock = pygame.time.Clock()
    menu = MainMenu()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    menu.selected_option = (menu.selected_option - 1) % len(menu.options)
                elif event.key == pygame.K_DOWN:
                    menu.selected_option = (menu.selected_option + 1) % len(menu.options)
                elif event.key == pygame.K_RETURN:
                    if menu.selected_option == 0:
                        print("Iniciar Jogo selecionado")
                        # Aqui você mudaria o estado do jogo para "JOGANDO"
                    elif menu.selected_option == 1:
                        print("Readme selecionado")
                    elif menu.selected_option == 2:
                        running = False

        screen.fill((0, 0, 0))  # Limpa a tela
        menu.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

# PONTO DE ENTRADA DO PROGRAMA
if __name__ == "__main__":
    main()