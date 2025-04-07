# -*- coding: utf-8 -*-
import pygame
import random
import math
from monstro import MonstroAnimado  # em vez de monstro.py
from funcoes import (resource_path, carregar_imagem, gerar_posicao_spawn)

class GerenciadorWaves:
    def __init__(self, tempo_duracao_wave=15, tempo_descanso=5):
        self.wave_atual = 1
        self.tempo_duracao_wave = tempo_duracao_wave  # Agora 15 segundos por wave
        self.tempo_descanso = tempo_descanso          # Descanso de 5 segundos
        self.wave_em_andamento = False
        self.tempo_inicio_wave = 0
        self.tempo_inicio_descanso = 0

        # Adicionando um "timer" para controlar a frequência de spawn (em segundos).
        # 50 ms = 0.05 s.
        self.tempo_ultimo_spawn = 0
        self.intervalo_spawn = 0.002  # 0.2 ms

    def iniciar_wave(self):
        self.wave_em_andamento = True
        self.tempo_inicio_wave = pygame.time.get_ticks() / 1000  # em segundos

    def finalizar_wave(self):
        self.wave_em_andamento = False
        self.tempo_inicio_descanso = pygame.time.get_ticks() / 1000

    def gerar_posicao_spawn_dentro_tela(self, centro, largura, altura, margem=10):
        """
        Gera uma posição de spawn dentro da tela, posicionando o monstro
        no máximo possível a partir do 'centro' (ex: posição do herói),
        antes de sair da tela.
        """
        cx, cy = centro
        angle = random.uniform(0, 2 * math.pi)
        
        # Calcular a distância máxima até a borda no eixo x
        if math.cos(angle) > 0:
            t_x = (largura - cx) / math.cos(angle)
        elif math.cos(angle) < 0:
            t_x = (0 - cx) / math.cos(angle)
        else:
            t_x = float('inf')
        
        # Calcular a distância máxima até a borda no eixo y
        if math.sin(angle) > 0:
            t_y = (altura - cy) / math.sin(angle)
        elif math.sin(angle) < 0:
            t_y = (0 - cy) / math.sin(angle)
        else:
            t_y = float('inf')
        
        # A distância máxima possível é a menor dessas duas
        t_max = min(t_x, t_y)
        spawn_distance = max(t_max - margem, 0)
        x = cx + spawn_distance * math.cos(angle)
        y = cy + spawn_distance * math.sin(angle)
        return (x, y)

    def atualizar(self, heroi, lista_monstros, largura_tela, altura_tela):
        """
        Atualiza a lógica das waves, incluindo o spawn de monstros.
        
        Durante 15 segundos, os monstros são gerados com uma probabilidade que 
        aumenta conforme a wave. Cada monstro spawna na posição máxima possível 
        dentro da tela (antes de sair dela), a partir da posição do herói.
        """
        tempo_corrente = pygame.time.get_ticks() / 1000
        
        if self.wave_em_andamento:
            tempo_passado_wave = tempo_corrente - self.tempo_inicio_wave
            
            if tempo_passado_wave >= self.tempo_duracao_wave:
                self.finalizar_wave()
                self.wave_atual += 1
            else:
                # A cada intervalo de 50ms, vamos verificar se devemos dar spawn.
                if tempo_corrente - self.tempo_ultimo_spawn >= self.intervalo_spawn:
                    # Probabilidade que aumenta com cada wave
                    probabilidade_spawn = 0.02 + (self.wave_atual * 0.05)
                    if random.random() < probabilidade_spawn:
                        # Gera a posição de spawn na borda interna da tela, a partir do herói.
                        pos_spawn_tela = self.gerar_posicao_spawn_dentro_tela(
                            (heroi.rect_heroi.centerx, heroi.rect_heroi.centery),
                            largura_tela,
                            altura_tela,
                            margem=100
                        )
                        
                        # Converte a posição de tela para posição no mundo.
                        spawn_mundo_x = pos_spawn_tela[0] + heroi.camera_x
                        spawn_mundo_y = pos_spawn_tela[1] + heroi.camera_y

                        # Ajusta a vida e o ataque dos monstros conforme a wave.
                        vida_base = 30 + (10 * self.wave_atual)
                        ataque_base = 5 + (3 * self.wave_atual)

                        monstro = MonstroAnimado(
                            (spawn_mundo_x, spawn_mundo_y),
                            vida_base,
                            ataque_base
                        )
                        lista_monstros.append(monstro)
                    
                    # Registra o último tempo em que tentamos dar spawn.
                    self.tempo_ultimo_spawn = tempo_corrente
        else:
            # Durante o período de descanso, aguardamos antes de iniciar a próxima wave.
            tempo_passado_descanso = tempo_corrente - self.tempo_inicio_descanso
            if tempo_passado_descanso >= self.tempo_descanso:
                self.iniciar_wave()

    def tempo_restante_wave(self):
        """
        Retorna o tempo restante da wave ou 0 se não estiver em andamento.
        """
        if self.wave_em_andamento:
            tempo_corrente = pygame.time.get_ticks() / 1000
            tempo_passado = tempo_corrente - self.tempo_inicio_wave
            restante = self.tempo_duracao_wave - tempo_passado
            return max(restante, 0)
        else:
            return 0
