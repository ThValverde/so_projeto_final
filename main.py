# main.py
# Ponto de entrada da aplicação. Gerencia o fluxo entre as telas (estados).

# Importa as classes das telas e a função principal do jogo
from ui.menu import MenuPrincipal
from ui.screens import TelaCarregamento, TelaFinal
from game.main_game import loop_do_jogo

def main():
    """ Função principal que controla o estado do jogo. """
    
    # Dicionário para mapear estados a objetos/funções
    telas = {
        "MENU": MenuPrincipal(),
        "LOADING": TelaCarregamento(),
        "PLAYING": loop_do_jogo, # Note que aqui é a função, não uma instância
        "FINAL_SCREEN": TelaFinal()
    }
    
    estado_atual = "MENU"
    
    while estado_atual != "EXITING":
        controlador = telas[estado_atual]
        
        # Se for uma classe (tem método 'run'), chama o método.
        # Se for uma função (como loop_do_jogo), apenas a chama.
        if hasattr(controlador, 'run'):
            proximo_estado = controlador.run()
        else:
            proximo_estado = controlador()
            
        estado_atual = proximo_estado

    print("\nSaindo da Oficina do Noel. Feliz Natal!")

if __name__ == "__main__":
    main()