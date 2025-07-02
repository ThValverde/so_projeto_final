# settings.py
# Este arquivo contém as configurações principais do jogo.

# Configurações de PATH
import os
PASTA_RAIZ = os.path.dirname(os.path.abspath(__file__))  # Caminho absoluto da pasta raiz do projeto
PASTA_ASSETS = os.path.join(PASTA_RAIZ, "assets")  # Pasta de assets
PASTA_IMAGENS = os.path.join(PASTA_ASSETS, "images")  # Pasta de imagens
PASTA_AUDIO = os.path.join(PASTA_ASSETS, "audio")  # Pasta de áudio
PASTA_FONTS = os.path.join(PASTA_ASSETS, "fonts")  # Pasta de fontes

FONTE_PATH = os.path.join(PASTA_FONTS, "pixel_operator", "PixelOperator.ttf")
FONTE_BOLD_PATH = os.path.join(PASTA_FONTS, "pixel_operator", "PixelOperator-Bold.ttf")
# Configurações de tela (serão usadas para o Pygame)

LARGURA_TELA = 800  # Largura da tela
ALTURA_TELA = 600  # Altura da tela
FPS = 60  # Frames por segundo


# Configurações de Gameplay
VAGAS_NA_MESA = 3 # Número de vagas na mesa de jogo

# Cores
BRANCO = (255, 255, 255)  # Branco
PRETO = (0, 0, 0)  # Preto
VERMELHO = (255, 0, 0)  # Vermelho
VERDE_ESCURO = (0, 100, 0)  # Verde escuro
VERDE_CLARO = (0, 128, 0)  # Verde claro
AZUL = (0, 0, 255)  # Azul
AMARELO = (255, 255, 0)  # Amarelo
CINZA = (128, 128, 128)  # Cinza
LARANJA = (255, 165, 0)  # Laranja
ROXO = (128, 0, 128)  # Roxo
PRETO_TRANSPARENTE = (0, 0, 0, 128)  # Preto semi-transparente



AUDIO_LOADING_1 = "loading_sound_1.mp3"
AUDIO_LOADING_2 = "loading_sound_2.mp3"
AUDIO_LOADING_3 = "loading_sound_3.mp3"
AUDIO_EXPLICACAO_JOGO = "explicacao_mecanicas.mp3"
AUDIO_MUSICA_FUNDO = "christmas-dreams-jingle-bells-268299.mp3"
