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

def game_loop(screen, clock):
    """
    Função que contém o loop principal do jogo completo com mecânicas de SO.

    Args:
        screen (pygame.Surface): A superfície principal da tela do jogo.
        clock (pygame.time.Clock): O objeto de relógio do Pygame para controlar o FPS.
    """
    # --- Inicialização das Mecânicas de SO ---
    game_mechanics = GameMechanics()
    game_mechanics.iniciar_sistema()
    
    # --- Configuração dos Elementos do Jogo ---
    background = GameBackground()
    all_sprites = pygame.sprite.Group()
    presentes_sprites = pygame.sprite.Group()  # Grupo para presentes caindo
    
    # --- Configuração das Esteiras ---
    y_pos_esteiras = ALTURA_TELA/4

    espacamento_horizontal_esteiras = 180
    largura_esteira = 200
    altura_esteira = 60
    x_pos_inicial_esteiras = (-60 + (LARGURA_TELA - (2 * espacamento_horizontal_esteiras) - largura_esteira) / 2)
    
    esteiras = [
        Esteira(position=(x_pos_inicial_esteiras, y_pos_esteiras), size=(largura_esteira, altura_esteira)),
        Esteira(position=(x_pos_inicial_esteiras + espacamento_horizontal_esteiras, y_pos_esteiras), size=(largura_esteira, altura_esteira)),
        Esteira(position=(x_pos_inicial_esteiras + espacamento_horizontal_esteiras * 2, y_pos_esteiras), size=(largura_esteira, altura_esteira))
    ]
    all_sprites.add(esteiras)

    # --- Configuração da Mesa de Presentes ---
    mesa_sprite = MesaDePresentes(position=(x_pos_inicial_esteiras + espacamento_horizontal_esteiras*3 + 30, ALTURA_TELA * 0.8))
    all_sprites.add(mesa_sprite)

    # --- Configuração do Elfo ---
    y_pos_elfo = ALTURA_TELA * 0.85
    POSICOES_ELFO = [
        (esteiras[0].rect.centerx, y_pos_elfo),
        (esteiras[1].rect.centerx, y_pos_elfo),
        (esteiras[2].rect.centerx, y_pos_elfo),
        (mesa_sprite.rect.centerx, y_pos_elfo)
    ]
    player = Elfo(positions=POSICOES_ELFO, start_index=0)
    all_sprites.add(player)
    
    # --- Variáveis de Controle do Jogo ---
    elfo_carregando_presente = False
    presente_carregado = None
    debug_mode = False  # Para mostrar informações de debug
    
    # --- Configuração de Fonte para UI ---
    try:
        from ..settings import FONTE_PATH
        font = pygame.font.Font(FONTE_PATH, 24)
        font_small = pygame.font.Font(FONTE_PATH, 18)
    except:
        font = pygame.font.Font(None, 24)
        font_small = pygame.font.Font(None, 18)
    # --- Loop Principal do Jogo ---
    running = True
    
    # Timer para gerar presentes visuais
    ultimo_spawn_presente = pygame.time.get_ticks()
    intervalo_spawn = 1500  # 1.5 segundos para melhor gameplay
    
    while running:
        current_time = pygame.time.get_ticks()
        
        # --- Processamento de Eventos ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_mechanics.parar_sistema()
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                # Controles do Elfo
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.move("left")
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.move("right")
                
                # Ação principal - coletar/entregar presente
                elif event.key == pygame.K_SPACE:
                    if not elfo_carregando_presente:
                        # Tentar coletar presente
                        if player.position_index < 3:  # Está em uma esteira
                            # Verifica se há presente caindo nesta posição
                            esteira_atual = esteiras[player.position_index]
                            for presente in presentes_sprites:
                                if (abs(presente.rect.centerx - player.rect.centerx) < 50 and 
                                    presente.rect.bottom >= player.rect.top - 20):
                                    # Coletou o presente
                                    presente.kill()
                                    elfo_carregando_presente = True
                                    presente_carregado = presente
                                    print("Presente coletado!")
                                    break
                    else:
                        # Tentar entregar presente na mesa
                        if player.position_index == 3:  # Está na mesa
                            if game_mechanics.adicionar_presente_mesa(presente_carregado):
                                mesa_sprite.adicionar_presente_visual()
                                elfo_carregando_presente = False
                                presente_carregado = None
                                print("Presente entregue na mesa!")
                            else:
                                print("Mesa cheia! Não foi possível entregar.")
                
                # Coletar da mesa (simula processamento manual)
                elif event.key == pygame.K_c:
                    if player.position_index == 3 and not elfo_carregando_presente:
                        if game_mechanics.elfo_tentar_coletar():
                            mesa_sprite.remover_presente_visual()
                            print("Presente coletado da mesa!")
                
                # Forçar processamento da mesa (tecla P)
                elif event.key == pygame.K_p:
                    if player.position_index == 3:  # Deve estar na mesa
                        if mesa_sprite.processar_presente():
                            print("Processamento manual iniciado!")
                        else:
                            print("Nenhum presente para processar ou já processando!")
                
                # Alternar processamento automático (tecla T)
                elif event.key == pygame.K_t:
                    if mesa_sprite.processamento_ativo:
                        mesa_sprite.desativar_processamento_automatico()
                    else:
                        mesa_sprite.ativar_processamento_automatico()
                
                # Acelerar processamento (tecla +)
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    novo_tempo = max(500, mesa_sprite.tempo_processamento - 500)
                    mesa_sprite.ajustar_velocidade_processamento(novo_tempo)
                
                # Desacelerar processamento (tecla -)
                elif event.key == pygame.K_MINUS:
                    novo_tempo = mesa_sprite.tempo_processamento + 500
                    mesa_sprite.ajustar_velocidade_processamento(novo_tempo)
                
                # Debug mode (tecla F1)
                elif event.key == pygame.K_F1:
                    debug_mode = not debug_mode
                    print(f"Debug mode: {'ON' if debug_mode else 'OFF'}")

        # --- Processamento de Novos Presentes das Threads ---
        novos_presentes = game_mechanics.processar_novos_presentes()
        
        # --- Geração Visual de Presentes ---
        if current_time - ultimo_spawn_presente > intervalo_spawn and len(presentes_sprites) < 6:
            # Escolhe esteira aleatória
            esteira_escolhida = random.choice(esteiras)
            
            # Cria presente visual
            novo_presente = Presente(esteira_escolhida, fall_speed=2)
            presentes_sprites.add(novo_presente)
            all_sprites.add(novo_presente)
            
            ultimo_spawn_presente = current_time

        # --- Atualização de Sprites ---
        all_sprites.update()
        if mesa_sprite.verificar_processamento_concluido():
            # 1. Tenta remover o item da LÓGICA DE CONTROLE (libera o semáforo)
            if game_mechanics.elfo_tentar_coletar():
                # 2. Se a lógica foi bem-sucedida, remove o item VISUAL
                mesa_sprite.finalizar_processamento_visual()
                
                # 3. Atualiza o timer para o próximo processamento automático
                mesa_sprite.ultimo_processamento = pygame.time.get_ticks()
                print("[SINCRONIA] Item processado e semáforo liberado.")
            else:
                # Caso de segurança: visualmente havia um item, mas logicamente não.
                # Apenas finaliza o estado visual.
                mesa_sprite.finalizar_processamento_visual()
                print("[AVISO] Sincronia corrigida: item visual removido sem contrapartida lógica.")

        # Remove presentes que saíram da tela
        for presente in presentes_sprites:
            if presente.rect.top > ALTURA_TELA:
                presente.kill()
                game_mechanics.presentes_perdidos += 1

        # --- Renderização ---
        background.draw(screen)
        all_sprites.draw(screen)
       # --- Interface do Usuário ---
        
        # (NOVO) Define e desenha os painéis de fundo para a HUD
        # Painel para as estatísticas da esquerda
        hud_stats_bg_rect = pygame.Rect(5, 5, 200, 195)
        stats_surface = pygame.Surface(hud_stats_bg_rect.size, pygame.SRCALPHA)
        stats_surface.fill(PRETO_TRANSPARENTE)
        screen.blit(stats_surface, hud_stats_bg_rect.topleft)

        # Painel para as instruções da direita
        hud_instructions_bg_rect = pygame.Rect(LARGURA_TELA - 230, 5, 225, 215)
        instructions_surface = pygame.Surface(hud_instructions_bg_rect.size, pygame.SRCALPHA)
        instructions_surface.fill(PRETO_TRANSPARENTE)
        screen.blit(instructions_surface, hud_instructions_bg_rect.topleft)
        
        # O resto do código da HUD continua, desenhando o texto por cima dos painéis
        stats = game_mechanics.get_estatisticas()
        
        # Pontuação
        texto_pontuacao = font.render(f"Pontuação: {stats['pontuacao']}", True, BRANCO)
        screen.blit(texto_pontuacao, (10, 10))
        
        # Nível
        texto_nivel = font.render(f"Nível: {stats['nivel_dificuldade']}", True, BRANCO)
        screen.blit(texto_nivel, (10, 40))
        
        # Status da mesa (expandido)
        mesa_info = stats['mesa_status']
        texto_mesa = font_small.render(f"Mesa: {mesa_info['presentes_na_mesa']}/{mesa_info['capacidade']}", True, BRANCO)
        screen.blit(texto_mesa, (10, 70))
        
        # Status do processamento da mesa
        status_proc = "ATIVO" if mesa_sprite.processamento_ativo else "PAUSADO"
        cor_status = VERDE_ESCURO if mesa_sprite.processamento_ativo else VERMELHO
        texto_proc_status = font_small.render(f"Proc. Auto: {status_proc}", True, cor_status)
        screen.blit(texto_proc_status, (10, 90))
        
        # Presentes processados pela mesa
        texto_processados = font_small.render(f"Processados: {mesa_sprite.presentes_processados_total}", True, BRANCO)
        screen.blit(texto_processados, (10, 110))
        
        # Velocidade de processamento
        velocidade_seg = mesa_sprite.tempo_processamento / 1000.0
        texto_velocidade = font_small.render(f"Vel. Proc: {velocidade_seg:.1f}s", True, BRANCO)
        screen.blit(texto_velocidade, (10, 130))
        
        # Presentes perdidos
        texto_perdidos = font_small.render(f"Perdidos: {stats['presentes_perdidos']}", True, VERMELHO)
        screen.blit(texto_perdidos, (10, 150))
        
        # Contador de presentes ativos na tela
        presentes_ativos = len(presentes_sprites)
        texto_presentes_ativos = font_small.render(f"Presentes Caindo: {presentes_ativos}", True, (255, 255, 0))
        screen.blit(texto_presentes_ativos, (10, 170))
        
        # Indicador se mesa está processando
        if mesa_sprite.processando:
            tempo_restante = (mesa_sprite.tempo_processamento - (pygame.time.get_ticks() - mesa_sprite.tempo_inicio_processamento)) / 1000.0
            tempo_restante = max(0, tempo_restante)
            texto_processando = font_small.render(f"Processando... {tempo_restante:.1f}s", True, (255, 255, 0))
            screen.blit(texto_processando, (mesa_sprite.rect.centerx - 60, mesa_sprite.rect.top - 50))
        
        # Indicador se elfo está carregando
        if elfo_carregando_presente:
            texto_carregando = font_small.render("Carregando Presente!", True, VERDE_ESCURO)
            screen.blit(texto_carregando, (player.rect.centerx - 70, player.rect.top - 30))
        
        # Instruções (expandidas)
        instrucoes = [
            "=== MOVIMENTO ===",
            "SETAS/WASD: Mover",
            "=== AÇÕES ===", 
            "ESPAÇO: Coletar/Entregar",
            "C: Processar da Mesa",
            "P: Forçar Processamento",
            "=== CONTROLES MESA ===",
            "T: Toggle Auto-Proc",
            "+/-: Vel. Processamento",
            "F1: Debug Mode",
            "ESC: Sair"
        ]
        
        for i, instrucao in enumerate(instrucoes):
            texto = font_small.render(instrucao, True, BRANCO)
            screen.blit(texto, (LARGURA_TELA - 220, 10 + i * 18))
        
        # Informações de debug (se ativado)
        if debug_mode:
            # (NOVO) Fundo para o painel de debug
            debug_bg_rect = pygame.Rect(LARGURA_TELA - 230, 230, 225, 120)
            debug_surface = pygame.Surface(debug_bg_rect.size, pygame.SRCALPHA)
            debug_surface.fill(PRETO_TRANSPARENTE)
            screen.blit(debug_surface, debug_bg_rect.topleft)

            debug_info = mesa_sprite.debug_status()
            debug_y = 240
            debug_texts = [
                f"DEBUG - Mesa Status:",
                f"Presentes: {debug_info['presentes_na_mesa']}",
                f"Auto-Proc: {debug_info['processamento_ativo']}",
                f"Processando: {debug_info['processando']}",
                f"Tempo desde último: {debug_info['tempo_desde_ultimo']}ms",
                f"Intervalo: {debug_info['tempo_processamento']}ms",
                f"Pode processar: {debug_info['pode_processar']}"
            ]
            
            for i, texto in enumerate(debug_texts):
                cor = VERDE_ESCURO if i == 0 else BRANCO
                debug_render = font_small.render(texto, True, cor)
                screen.blit(debug_render, (LARGURA_TELA - 220, debug_y + i * 16))
        
        # Informações de debug (se ativado)
        if debug_mode:
            debug_info = mesa_sprite.debug_status()
            debug_y = 220
            debug_texts = [
                f"DEBUG - Mesa Status:",
                f"Presentes: {debug_info['presentes_na_mesa']}",
                f"Auto-Proc: {debug_info['processamento_ativo']}",
                f"Processando: {debug_info['processando']}",
                f"Tempo desde último: {debug_info['tempo_desde_ultimo']}ms",
                f"Intervalo: {debug_info['tempo_processamento']}ms",
                f"Pode processar: {debug_info['pode_processar']}"
            ]
            
            for i, texto in enumerate(debug_texts):
                cor = VERDE_ESCURO if i == 0 else BRANCO
                debug_render = font_small.render(texto, True, cor)
                screen.blit(debug_render, (LARGURA_TELA - 220, debug_y + i * 16))

        pygame.display.flip()
        clock.tick(FPS)
    
    # --- Limpeza ---
    game_mechanics.parar_sistema()
    print("Jogo finalizado!")