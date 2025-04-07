# -*- coding: utf-8 -*-
import pygame
import math
import os
from random import random
from funcoes import (resource_path, carregar_imagem)
from configuracoes import (
    TAMANHO_SPRITE_MONSTRO,
    ITEM_CURA,
    ITEM_XP,
    TAMANHO_SPRITE_ITEM,
    TEMPO_EFEITO_DANO
)

def carregar_frames(pasta, prefixo, quantidade, largura=None, altura=None):
    """
    Carrega uma sequência de imagens numeradas, como:
    prefixo_001.png, prefixo_002.png, ... prefixo_n.png
    de 1 até 'quantidade'.
    Se largura e altura forem especificados, redimensiona cada imagem.
    Retorna uma lista de Surfaces.
    """
    frames = []
    for i in range(1, quantidade + 1):
        nome_arquivo = f"{prefixo}_{i}.png"
        caminho_completo = os.path.join(pasta, nome_arquivo)
        imagem = carregar_imagem(caminho_completo, largura, altura)
        frames.append(imagem)
    return frames

class Item:
    def __init__(self, tipo, posicao, frames):
        self.tipo = tipo  # 'xp' ou 'vida'
        self.posicao = posicao  # Posição no mundo (x, y)
        self.frames = frames  # Lista de frames da animação
        self.frame_atual = 0
        self.tempo_ultimo_frame = pygame.time.get_ticks()
        self.tempo_por_frame = 100  # Tempo entre cada frame (em ms)
        self.rect = pygame.Rect(0, 0, 5, 5)  # Tamanho do item
        self.rect.center = posicao
        self.velocidade = 1.5  # Velocidade de movimento em direção ao herói

    def update(self, heroi_pos, heroi_rect):
        """
        Atualiza a animação e o movimento do item em direção ao herói.
        Retorna True se o item foi coletado pelo herói.
        """
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.tempo_ultimo_frame > self.tempo_por_frame:
            self.frame_atual = (self.frame_atual + 1) % len(self.frames)
            self.tempo_ultimo_frame = tempo_atual

        dx = heroi_pos[0] - self.posicao[0]
        dy = heroi_pos[1] - self.posicao[1]
        distancia = math.hypot(dx, dy)

        if distancia > 0:
            self.posicao = (
                self.posicao[0] + (dx / distancia) * self.velocidade,
                self.posicao[1] + (dy / distancia) * self.velocidade
            )
            self.rect.center = self.posicao

        heroi_rect_mundo = pygame.Rect(
            heroi_pos[0] - heroi_rect.width // 2,
            heroi_pos[1] - heroi_rect.height // 2,
            heroi_rect.width,
            heroi_rect.height
        )

        if self.rect.colliderect(heroi_rect_mundo):
            return True
        return False

    def draw(self, tela, camera_x, camera_y):
        x_tela = self.posicao[0] - camera_x
        y_tela = self.posicao[1] - camera_y
        tela.blit(self.frames[self.frame_atual], (x_tela, y_tela))

class MonstroAnimado:
    def __init__(self, posicao_inicial_mundo, vida_base, ataque_base, nivel_heroi=1):
        self.vida = vida_base + (nivel_heroi - 1) * 10
        self.ataque = ataque_base + (nivel_heroi - 1) * 2

        self.chance_drop_vida = 1 / 100
        self.chance_drop_xp = 1

        self.frames_drop_vida = carregar_frames("assets/Drop/Vida", "Vida", 8, TAMANHO_SPRITE_ITEM[0], TAMANHO_SPRITE_ITEM[1])
        self.frames_drop_xp = carregar_frames("assets/Drop/XP", "XP", 10, TAMANHO_SPRITE_ITEM[0], TAMANHO_SPRITE_ITEM[1])

        self.x_mundo = posicao_inicial_mundo[0]
        self.y_mundo = posicao_inicial_mundo[1]
        self.velocidade = 1.5
        self.frames_andando = carregar_frames("assets/Monstro/Monstro_andando", "Andando", 2, TAMANHO_SPRITE_MONSTRO[0], TAMANHO_SPRITE_MONSTRO[1])
        self.frames_hit = carregar_frames("assets/Monstro/Monstro_Hit", "hit", 1, TAMANHO_SPRITE_MONSTRO[0], TAMANHO_SPRITE_MONSTRO[1])
        self.estado = 'walk'
        self.frame_atual = 0
        self.tempo_ultimo_frame = pygame.time.get_ticks()
        self.tempo_por_frame = 200
        self.tempo_efeito_dano = 0
        self.rect = pygame.Rect(0, 0, TAMANHO_SPRITE_MONSTRO[0], TAMANHO_SPRITE_MONSTRO[1])
        self.imagem_atual = None
        self.atualizar_imagem()
        self.alpha = 255
        self.tempo_morte = None
        # Inicializamos o tempo do último hit para 0 (ou um valor antigo)
        self.tempo_hit = 0

    def drop_item(self):
        if random() <= self.chance_drop_vida:
            return Item('vida', (self.x_mundo, self.y_mundo), self.frames_drop_vida)
        else:
            return Item('xp', (self.x_mundo, self.y_mundo), self.frames_drop_xp)

    def atualizar_imagem(self):
        tempo_atual = pygame.time.get_ticks()

        if self.estado == 'walk':
            frames = self.frames_andando
        elif self.estado == 'hit' or self.estado == 'dying':
            frames = self.frames_hit
        else:
            frames = self.frames_andando

        if len(frames) == 0:
            self.imagem_atual = None
            return
        
        self.frame_atual %= len(frames)
        self.imagem_atual = frames[self.frame_atual]
        self.rect.size = self.imagem_atual.get_size()

    def update_animacao(self):
        tempo_atual = pygame.time.get_ticks()
        if self.estado == 'dying':
            return
        # Se já se passaram 750 ms desde o último hit, retorna ao estado 'walk'
        if self.estado == 'hit' and (tempo_atual - self.tempo_hit) >= 750:
            self.estado = 'walk'
        if (tempo_atual - self.tempo_ultimo_frame) > self.tempo_por_frame:
            self.frame_atual += 1
            self.tempo_ultimo_frame = tempo_atual
            self.atualizar_imagem()

    def mover_em_direcao(self, alvo_x_mundo, alvo_y_mundo):
        if self.estado != 'dying':
            dx = alvo_x_mundo - self.x_mundo
            dy = alvo_y_mundo - self.y_mundo
            distancia = math.hypot(dx, dy)

            if distancia > 0:
                self.x_mundo += (self.velocidade * dx / distancia)
                self.y_mundo += (self.velocidade * dy / distancia)
                self.flip = (dx > 0)

    def atualizar_rect(self, camera_x, camera_y):
        self.rect.centerx = self.x_mundo - camera_x
        self.rect.centery = self.y_mundo - camera_y

    def update(self, tela):
        self.update_animacao()
        
        if self.vida <= 0:
            if self.tempo_morte is None:
                self.tempo_morte = pygame.time.get_ticks()
                self.estado = 'dying'
                # Armazena o item dropado, mas não retorna imediatamente
                self.item_dropado = self.drop_item()
            tempo_decorrido = pygame.time.get_ticks() - self.tempo_morte
            duracao_fade_out = 1000  # 1 segundo para o fade-out
            self.alpha = max(255 - int((tempo_decorrido / duracao_fade_out) * 255), 0)
            
            if self.alpha == 0:
                # Retorna o item dropado (ou True, conforme a lógica do jogo) apenas após o fade-out completo
                return self.item_dropado
            return False  # Ainda em fade-out
        return False


    def desenhar(self, tela):
        if self.imagem_atual:
            imagem_com_efeito = self.imagem_atual.copy()
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_efeito_dano < TEMPO_EFEITO_DANO:
                vermelho = pygame.Surface(imagem_com_efeito.get_size(), pygame.SRCALPHA)
                vermelho.fill((255, 0, 0, 200))
                imagem_com_efeito.blit(vermelho, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

            if hasattr(self, "flip") and self.flip:
                imagem_com_efeito = pygame.transform.flip(imagem_com_efeito, True, False)

            if self.alpha < 255:
                imagem_com_efeito.set_alpha(self.alpha)

            tela.blit(imagem_com_efeito, self.rect)

    def receber_dano(self, dano):
        # Só permite dano se já se passaram 250 ms desde o último hit
        tempo_atual = pygame.time.get_ticks()
        if (tempo_atual - self.tempo_hit) < 250:
            return

        self.vida -= dano
        if self.vida < 0:
            self.vida = 0

        self.estado = 'hit'
        self.frame_atual = 0
        self.tempo_hit = tempo_atual  # Registra o instante do hit
        self.tempo_efeito_dano = tempo_atual
        self.atualizar_imagem()

    def receber_golpe_especial(self):
        self.vida = 0

    def esta_vivo(self):
        return self.vida > 0
