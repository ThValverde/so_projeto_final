# game/integration_example.py
# Exemplo de como as mecânicas de SO se integram no jogo

"""
EXEMPLO DE INTEGRAÇÃO DAS MECÂNICAS DE SISTEMAS OPERACIONAIS

Este arquivo demonstra como os conceitos de SO são aplicados no jogo:

=== CONCEITOS IMPLEMENTADOS ===

1. THREADS PRODUTORAS (Producer)
   - Cada esteira tem uma thread que produz presentes continuamente
   - Simula processos produtores em um sistema real
   - Threads rodam em paralelo com o jogo principal

2. SEMÁFOROS (Semaphore)
   - Mesa de presentes tem capacidade limitada (3 vagas)
   - Semáforo controla acesso concorrente à mesa
   - Elfo deve aguardar vaga disponível para entregar

3. PROBLEMA PRODUTOR-CONSUMIDOR
   - Produtores: Esteiras gerando presentes
   - Consumidor: Elfo coletando e processando
   - Buffer: Mesa de presentes com capacidade limitada

4. ESCALONAMENTO
   - Escalonador aumenta dificuldade periodicamente
   - Simula algoritmos de escalonamento de CPU
   - Balanceia carga entre diferentes produtores

5. SEÇÕES CRÍTICAS
   - Acesso à mesa protegido por mutex
   - Operações atômicas para adicionar/remover presentes
   - Previne condições de corrida

=== FLUXO DO JOGO ===

1. Início: 3 threads produtoras iniciam (uma por esteira)
2. Produção: Threads criam presentes e os colocam na fila
3. Visualização: Jogo processa fila e cria sprites visuais
4. Coleta: Jogador move elfo para coletar presentes
5. Entrega: Elfo tenta entregar na mesa (controlada por semáforo)
6. Processamento: Elfo pode processar presentes da mesa
7. Escalonamento: Dificuldade aumenta automaticamente

=== CONTROLES DO JOGO ===

SETAS/WASD: Mover elfo entre posições
ESPAÇO: Coletar presente (se estiver em esteira) OU entregar na mesa
C: Processar presente da mesa (simula consumo)
ESC: Sair do jogo

=== DEMONSTRAÇÃO DE CONCEITOS ===

- DEADLOCK: Se mesa ficar cheia, produção para até ser processada
- STARVATION: Esteiras competem por atenção do elfo
- THROUGHPUT: Pontuação baseada em presentes processados
- LATÊNCIA: Tempo entre produção e processamento

=== MÉTRICAS EXIBIDAS ===

- Pontuação: Total de presentes processados
- Nível: Indica velocidade de produção atual
- Mesa: Ocupação atual da mesa (semáforo)
- Perdidos: Presentes que caíram sem ser coletados
- Threads ativas: Número de produtores funcionando

=== EXEMPLO DE USO DAS CLASSES ===

# Inicializar sistema
game_mechanics = GameMechanics()
game_mechanics.iniciar_sistema()

# Processar novos presentes das threads
novos_presentes = game_mechanics.processar_novos_presentes()

# Elfo tenta entregar na mesa (usa semáforo)
sucesso = game_mechanics.adicionar_presente_mesa(presente_data)

# Elfo processa da mesa (libera semáforo)
coletou = game_mechanics.elfo_tentar_coletar()

# Obter estatísticas
stats = game_mechanics.get_estatisticas()

# Finalizar (para todas as threads)
game_mechanics.parar_sistema()

=== OBSERVAÇÕES TÉCNICAS ===

1. Threads são marcadas como daemon para terminarem com o programa
2. Queue thread-safe é usada para comunicação entre threads
3. Semáforos controlam acesso ao recurso compartilhado (mesa)
4. Mutex protege seções críticas das operações
5. Escalonador simula preempção ajustando velocidades

Este exemplo educativo demonstra na prática como conceitos
teóricos de SO funcionam em um ambiente real de programação!
"""

# Exemplo prático de uso standalone
if __name__ == "__main__":
    import time
    from mechanics import GameMechanics
    
    print("=== DEMONSTRAÇÃO DAS MECÂNICAS ===")
    
    # Inicializa sistema
    mechanics = GameMechanics()
    mechanics.iniciar_sistema()
    
    print("Sistema iniciado! Threads produtoras trabalhando...")
    
    # Simula gameplay por 30 segundos
    for i in range(30):
        time.sleep(1)
        
        # Processa presentes criados
        novos = mechanics.processar_novos_presentes()
        if novos:
            print(f"Novos presentes criados: {len(novos)}")
        
        # Simula elfo coletando aleatoriamente
        if i % 3 == 0:
            mechanics.elfo_tentar_coletar()
        
        # Mostra estatísticas a cada 10 segundos
        if i % 10 == 0:
            stats = mechanics.get_estatisticas()
            print(f"Estatísticas: {stats}")
    
    # Para sistema
    mechanics.parar_sistema()
    print("Demonstração finalizada!")
