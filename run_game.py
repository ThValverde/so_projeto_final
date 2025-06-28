#!/usr/bin/env python3
"""
Script de entrada para o jogo "Oficina do Noel"
Execute este arquivo para iniciar o jogo.
"""

import sys
import os

# Adiciona o diretório pai ao path para permitir imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from so_projeto_final.main import main
    
    if __name__ == "__main__":
        print("=== OFICINA DO NOEL: OPERAÇÃO SINCRONIZADA ===")
        print("Iniciando o jogo...")
        main()
        
except ImportError as e:
    print(f"Erro de importação: {e}")
    print("Certifique-se de que está executando do diretório correto.")
except KeyboardInterrupt:
    print("\nJogo finalizado pelo usuário.")
except Exception as e:
    print(f"Erro inesperado: {e}")
    import traceback
    traceback.print_exc()
