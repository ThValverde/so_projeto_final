# game/main_game.py
# Contém a lógica principal do gameplay com mecânicas completas de SO.

import pygame
import sys
import random

# Importa as classes e configurações necessárias
from ..settings import LARGURA_TELA, ALTURA_TELA, FPS, BRANCO, PRETO, VERDE_ESCURO, VERMELHO, PRETO_TRANSPARENTE
from ..ui.screens import GameBackground
from .entities import Esteira, Elfo, MesaDePresentes, Presente
from .mechanics import GameMechanics

def game_loop(screen, clock, game_mechanics):
    """
    Função que contém o loop principal do jogo completo com mecânicas de SO.

    Args:
        screen (pygame.Surface): A superfície principal da tela do jogo.
        clock (pygame.time.Clock): O objeto de relógio do Pygame para controlar o FPS.
        game_mechanics (GameMechanics): A instância das mecânicas do jogo para a partida atual.
    """
    
    # --- Configuração dos Elementos do Jogo ---
    background = GameBackground()
    all_sprites = pygame.sprite.Group()
    presentes_sprites = pygame.sprite.Group()
    
    esteiras = [
        Esteira(position=(-60 + (LARGURA_TELA - 560) / 2, ALTURA_TELA/4), size=(200, 60)),
        Esteira(position=(-60 + (LARGURA_TELA - 560) / 2 + 180, ALTURA_TELA/4), size=(200, 60)),
        Esteira(position=(-60 + (LARGURA_TELA - 560) / 2 + 360, ALTURA_TELA/4), size=(200, 60))
    ]
    all_sprites.add(esteiras)

    mesa_sprite = MesaDePresentes(position=(-60 + (LARGURA_TELA - 560) / 2 + 570, ALTURA_TELA * 0.8))
    all_sprites.add(mesa_sprite)

    y_pos_elfo = ALTURA_TELA * 0.85
    POSICOES_ELFO = [
        (esteiras[0].rect.centerx, y_pos_elfo),
        (esteiras[1].rect.centerx, y_pos_elfo),
        (esteiras[2].rect.centerx, y_pos_elfo),
        (mesa_sprite.rect.centerx, y_pos_elfo)
    ]
    player = Elfo(positions=POSICOES_ELFO, start_index=0)
    all_sprites.add(player)
    
    debug_mode = False
    
    try:
        from ..settings import FONTE_PATH
        font = pygame.font.Font(FONTE_PATH, 24)
        font_small = pygame.font.Font(FONTE_PATH, 18)
    except:
        font = pygame.font.Font(None, 24)
        font_small = pygame.font.Font(None, 18)

    popup_ativo = False
    popup_surface = None
    popup_rect = None
    popup_duracao = 1500
    popup_tempo_final = 0
    
    running = True
    ultimo_spawn_presente = pygame.time.get_ticks()
    
    while running:
        current_time = pygame.time.get_ticks()
        
        if popup_ativo and current_time > popup_tempo_final:
            popup_ativo = False
            popup_surface = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'MENU'
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.move("left")
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.move("right")
                elif event.key == pygame.K_SPACE:
                    if player.position_index == 3:
                        if player.presentes_carregados > 0:
                            if game_mechanics.adicionar_presente_mesa(None):
                                mesa_sprite.adicionar_presente_visual()
                                player.descarregar_presente()
                            else:
                                popup_ativo = True
                                popup_tempo_final = current_time + popup_duracao
                                texto_popup = "MESA CHEIA: -1 presente"
                                popup_surface = font_small.render(texto_popup, True, VERMELHO) 
                                popup_rect = popup_surface.get_rect(center=(mesa_sprite.rect.centerx, mesa_sprite.rect.top - 25))
                    elif player.position_index < 3:
                        if player.presentes_carregados < player.capacidade_carga:
                            for presente in presentes_sprites:
                                if (abs(presente.rect.centerx - player.rect.centerx) < 50 and presente.rect.bottom >= player.rect.top - 20):
                                    presente.kill()
                                    player.carregar_presente()
                                    break
                elif event.key == pygame.K_p:
                    if player.position_index == 3:
                        mesa_sprite.processar_presente()
                # elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                #     mesa_sprite.ajustar_velocidade_processamento(max(500, mesa_sprite.tempo_processamento - 500))
                # elif event.key == pygame.K_MINUS:
                #     mesa_sprite.ajustar_velocidade_processamento(mesa_sprite.tempo_processamento + 500)
                elif event.key == pygame.K_F1:
                    debug_mode = not debug_mode

        intervalo_atual = game_mechanics.escalonador.taxa_spawn_atual
        if current_time - ultimo_spawn_presente > intervalo_atual and len(presentes_sprites) < 6:
            esteira_escolhida = random.choice(esteiras)
            velocidade_atual = game_mechanics.escalonador.velocidade_queda_atual
            novo_presente = Presente(esteira_escolhida, game_mechanics, fall_speed=velocidade_atual)
            presentes_sprites.add(novo_presente)
            all_sprites.add(novo_presente)
            ultimo_spawn_presente = current_time

        all_sprites.update()
        
        if mesa_sprite.verificar_processamento_concluido():
            if game_mechanics.elfo_tentar_coletar(player):
                mesa_sprite.finalizar_processamento_visual()
                mesa_sprite.ultimo_processamento = current_time
            else:
                mesa_sprite.finalizar_processamento_visual()
        
        # --- (BLOCO PROBLEMÁTICO REMOVIDO DAQUI) ---

        # --- Condições de Fim de Jogo (ÚNICA VERIFICAÇÃO CORRETA) ---
        if game_mechanics.pontuacao >= 300:
            print("="*30)
            print("VITÓRIA! Você atingiu 300 pontos!")
            print(f"Pontuação Final: {game_mechanics.pontuacao}")
            print(f"Presentes Perdidos: {game_mechanics.presentes_perdidos}")
            print("="*30)
            return 'VITORIA'

        if game_mechanics.verificar_derrota():
            print("="*30)
            print("FIM DE JOGO! Muitos presentes foram perdidos.")
            print(f"Pontuação Final: {game_mechanics.pontuacao}")
            print(f"Presentes Perdidos: {game_mechanics.presentes_perdidos}")
            print("="*30)
            return 'DERROTA'

        # --- Renderização ---
        background.draw(screen)
        all_sprites.draw(screen)
        player.desenhar_carga(screen)
        if popup_ativo:
            screen.blit(popup_surface, popup_rect)
        
        # --- HUD ---
        hud_stats_bg_rect = pygame.Rect(5, 5, 200, 205)
        stats_surface = pygame.Surface(hud_stats_bg_rect.size, pygame.SRCALPHA)
        stats_surface.fill(PRETO_TRANSPARENTE)
        screen.blit(stats_surface, hud_stats_bg_rect.topleft)
        
        hud_instructions_bg_rect = pygame.Rect(LARGURA_TELA - 230, 5, 225, 215)
        instructions_surface = pygame.Surface(hud_instructions_bg_rect.size, pygame.SRCALPHA)
        instructions_surface.fill(PRETO_TRANSPARENTE)
        screen.blit(instructions_surface, hud_instructions_bg_rect.topleft)
        
        stats = game_mechanics.get_estatisticas()
        
        textos_hud = [
            (f"Pontuação: {stats['pontuacao']}", (10, 10), font, BRANCO),
            (f"Nível: {stats['nivel_dificuldade']}", (10, 40), font, BRANCO),
            (f"Mesa: {stats['mesa_status']['presentes_na_mesa']}/{stats['mesa_status']['capacidade']}", (10, 70), font_small, BRANCO),
            (f"Proc. Auto: {'ATIVO' if mesa_sprite.processamento_ativo else 'PAUSADO'}", (10, 90), font_small, VERDE_ESCURO if mesa_sprite.processamento_ativo else VERMELHO),
            (f"Processados: {mesa_sprite.presentes_processados_total}", (10, 110), font_small, BRANCO),
            (f"Vel. Proc: {mesa_sprite.tempo_processamento / 1000.0:.1f}s", (10, 130), font_small, BRANCO),
            (f"Perdidos: {stats['presentes_perdidos']}", (10, 150), font_small, VERMELHO),
            (f"Penalidade: {stats['presentes_perdidos'] * 10}", (10, 170), font_small, VERMELHO),
            (f"Presentes Caindo: {len(presentes_sprites)}", (10, 190), font_small, (255, 255, 0))
        ]
        
        for texto, pos, fonte_obj, cor in textos_hud:
            render = fonte_obj.render(texto, True, cor)
            screen.blit(render, pos)

        if mesa_sprite.processando:
            tempo_restante = max(0, (mesa_sprite.tempo_processamento - (current_time - mesa_sprite.tempo_inicio_processamento)) / 1000.0)
            texto_processando = font_small.render(f"Processando... {tempo_restante:.1f}s", True, (255, 255, 0))
            screen.blit(texto_processando, (mesa_sprite.rect.centerx - 60, mesa_sprite.rect.top - 50))
        
        instrucoes = [
            "=== MOVIMENTO ===", "SETAS/WASD: Mover",
            "=== AÇÕES ===", "ESPAÇO: Coletar/Entregar", "P: Forçar Processamento",
            # "=== CONTROLES MESA ===", "+/-: Vel. Processamento",
            #"F1: Debug Mode", 
            "ESC: Sair"
        ]
        
        for i, instrucao in enumerate(instrucoes):
            texto = font_small.render(instrucao, True, BRANCO)
            screen.blit(texto, (LARGURA_TELA - 220, 10 + i * 18))
        
        if debug_mode:
            # ... (código de debug) ...
            pass

        pygame.display.flip()
        clock.tick(FPS)