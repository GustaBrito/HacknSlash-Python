# -*- coding: utf-8 -*-
import pygame
import random
import math
import os
import sys

def resource_path(relative_path):
    """
    Retorna o caminho absoluto para os recursos, seja durante o desenvolvimento
    ou quando empacotado pelo PyInstaller (utilizando sys._MEIPASS).
    """
    try:
        base_path = sys._MEIPASS  # PyInstaller extrai os arquivos para esta pasta temporária
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def carregar_imagem(caminho, largura=None, altura=None):
    """
    Carrega a imagem a partir do caminho (usando resource_path) e, se largura e altura forem informadas,
    redimensiona a imagem.
    """
    caminho_absoluto = resource_path(caminho)
    try:
        imagem = pygame.image.load(caminho_absoluto).convert_alpha()
    except Exception as e:
        print(f"Erro ao carregar imagem: {caminho_absoluto} - {e}")
        raise
    if largura is not None and altura is not None:
        imagem = pygame.transform.scale(imagem, (largura, altura))
    return imagem

def get_save_path(filename):
    # Verifica se o programa está empacotado
    if getattr(sys, 'frozen', False):
        # Usa o diretório onde o executável está localizado
        base_path = os.path.dirname(sys.executable)
    else:
        # Durante o desenvolvimento, usa o diretório atual
        base_path = os.getcwd()

    # Define o caminho desejado relativo ao base_path:
    # "HacknSlashUninter/assets/save"
    save_dir = os.path.join(base_path, "HacknSlashUninter")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    return os.path.join(save_dir, filename)



def gerar_posicao_spawn(centro_heroi_x, centro_heroi_y, largura_tela, altura_tela, borda=200):
    """
    Gera uma posição aleatória ao redor (fora) da área visível,
    simulando spawn infinito.
    """
    # Gera posição distante da tela (para simular monstros vindo "de fora")
    x_spawn = random.randint(-borda, largura_tela + borda)
    y_spawn = random.randint(-borda, altura_tela + borda)
    
    # Checa se está longe o suficiente do herói
    distancia = math.hypot(x_spawn - centro_heroi_x, y_spawn - centro_heroi_y)
    if distancia < 150:
        # Se cair muito perto, chama recursivamente
        return gerar_posicao_spawn(centro_heroi_x, centro_heroi_y, largura_tela, altura_tela, borda)
    
    return (x_spawn, y_spawn)

def carregar_frames(pasta, prefixo, quantidade):
    """
    Carrega uma sequência de imagens numeradas, como:
    prefixo_1.png, prefixo_2.png, ... prefixo_n.png
    de 1 até 'quantidade'.
    """
    frames = []
    for i in range(1, quantidade + 1):
        nome_arquivo = f"{prefixo}_{i}.png"  # ex.: "Parado_1.png"
        caminho_completo = os.path.join(pasta, nome_arquivo)
        imagem = carregar_imagem(caminho_completo)
        frames.append(imagem)
    return frames

def calcular_angulo_origem(dest_x, dest_y, origem_x, origem_y):
    """
    Calcula o ângulo (em radianos) do ponto de origem para o ponto de destino.
    Usado para rotacionar a espada (ou efeito de corte) em direção ao mouse.
    """
    dx = dest_x - origem_x
    dy = dest_y - origem_y
    angulo = math.atan2(dy, dx)  # atan2 retorna o ângulo em radianos
    return angulo

def colisao_corte_monstro(corte_rect, monstro_rect):
    """
    Verifica se o corte (hitbox do efeito) colide com o monstro.
    Usamos retângulos para simplificar (rects).
    """
    return corte_rect.colliderect(monstro_rect)

def desenhar_fundo_animado(tela, imagem_fundo, camera_x, camera_y, largura_tela, altura_tela):
    """
    Desenha um fundo "infinito" usando tiles.
    Baseado no offset (camera_x, camera_y), repete o tile de fundo
    em toda a área da tela.
    """
    # Tamanho do tile
    tile_largura = imagem_fundo.get_width()
    tile_altura = imagem_fundo.get_height()

    # Calcula o deslocamento com base na câmera
    # Ajuste: agora o fundo se move na mesma direção que o herói
    offset_x = camera_x % tile_largura
    offset_y = camera_y % tile_altura

    # Quantos tiles precisamos desenhar horizontal e verticalmente
    tiles_horiz = (largura_tela // tile_largura) + 2
    tiles_vert = (altura_tela // tile_altura) + 2

    for i in range(tiles_horiz):
        for j in range(tiles_vert):
            x = (i * tile_largura) - offset_x
            y = (j * tile_altura) - offset_y
            tela.blit(imagem_fundo, (x, y))