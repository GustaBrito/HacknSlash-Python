# -*- coding: utf-8 -*-
import pygame
from funcoes import (resource_path, carregar_imagem)

# Dimensões da tela
LARGURA_TELA = 1280
ALTURA_TELA = 720

# Cores
COR_PRETO = (0, 0, 0)
COR_BRANCO = (255, 255, 255)
COR_VERMELHO = (255, 0, 0)
COR_VERDE = (0, 255, 0)
COR_AMARELO = (255, 255, 0)
COR_AMARELO = (255, 255, 0)

# Inicialização do Pygame (poderia ficar no main, mas facilita o uso de fontes etc.)
pygame.init()

# Fonte padrão
FONTE_PADRAO = pygame.font.SysFont("arial", 18)

# FPS (frames por segundo)
FPS = 60

# Tempo de invencibilidade após sofrer dano (em milissegundos)
TEMPO_INVENCIBILIDADE = 500

# Tamanhos padronizados para os sprites
TAMANHO_SPRITE_HEROI = (128, 128)
TAMANHO_SPRITE_MONSTRO = (64, 64)
TAMANHO_SPRITE_CORTE = (256, 256)
TAMANHO_CURSOR = (35, 35)

# Coordenadas iniciais do herói (centralizado na tela)
HEROI_X_INICIAL = LARGURA_TELA // 2 - TAMANHO_SPRITE_HEROI[0] // 2
HEROI_Y_INICIAL = ALTURA_TELA // 2 - TAMANHO_SPRITE_HEROI[1] // 2

# Estados do jogo
ESTADO_MENU = 0
ESTADO_JOGANDO = 1
ESTADO_GAME_OVER = 2

# Textos do menu
TEXTO_MENU_TITULO = "Meu Jogo"
TEXTO_MENU_INICIAR = "Iniciar"
TEXTO_MENU_SAIR = "Sair"

COR_BOTAO_FUNDO = (30, 30, 30, 150)  # Fundo semi-transparente
COR_BOTAO_TEXTO = (255, 255, 255)    # Texto branco
COR_BOTAO_HOVER = (50, 50, 50, 200) # Fundo ao passar o mouse
COR_BOTAO_SELECIONADO = (0, 150, 255)  # Azul para botão selecionado

# Cores dos botões
COR_BOTAO_NORMAL = COR_VERDE
COR_BOTAO_SELECIONADO = COR_AMARELO

# Itens
ITEM_CURA = {"nome": "Cura", "valor": 20, "imagem": "cura.png", "chance": 1/100}
ITEM_XP = {"nome": "XP", "valor": 10, "imagem": "xp.png", "chance": 1}  # Sempre dropa

# Tamanho dos itens
TAMANHO_SPRITE_ITEM = (32, 32)

# Tempo de duração do efeito vermelho ao tomar dano (em milissegundos)
TEMPO_EFEITO_DANO = 200

# Opções de evolução
EVOLUCAO_FORCA = {"nome": "Força", "valor": 3}
EVOLUCAO_VIDA = {"nome": "Vida", "valor": 20}
EVOLUCAO_VELOCIDADE = {"nome": "Velocidade", "valor": 1}

# Textos do game over
TEXTO_GAME_OVER = "Game Over"
TEXTO_TEMPO_SOBREVIVIDO = "Tempo Sobrevivido: {}"
TEXTO_WAVE_ALCANCADA = "Wave Alcançada: {}"
TEXTO_NIVEL_MAXIMO = "Nível Máximo: {}"
TEXTO_VOLTAR_MENU = "Voltar ao Menu"
TEXTO_SAIR_JOGO = "Sair do Jogo"

# Golpe especial
TEMPO_RECARGA_GOLPE_ESPECIAL = 30000  # 30 segundos em milissegundos