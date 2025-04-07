# -*- coding: utf-8 -*-
import pygame
import os
from configuracoes import (COR_BRANCO, COR_VERMELHO, COR_VERDE, LARGURA_TELA, ALTURA_TELA)
from funcoes import (resource_path, carregar_imagem)

# Carrega uma fonte TTF customizada, se disponível. Ajuste o caminho conforme necessário.
CAMINHO_FONTE_CUSTOM = resource_path("assets/fonts/Bitwise.ttf")

try:
    FONTE_MODERNA = pygame.font.Font(CAMINHO_FONTE_CUSTOM, 20)
except:
    # Se não encontrar a fonte customizada, utiliza a fonte padrão do sistema.
    FONTE_MODERNA = pygame.font.SysFont("arial", 20)

habilidade_disponivel = False
proximo_trigger = 50

def desenhar_hud(tela, heroi, pontuacao, wave_atual, tempo_restante, cooldown_restante, wave_ativa):
    """
    Desenha na tela as informações de vida, XP, pontuação, horda e tempo (ou descanso).
    
    Parâmetros:
      tela             - a Surface principal do jogo;
      heroi            - objeto do herói (deve ter atributos: vida_atual, vida_maxima, xp_atual, xp_para_proximo_nivel, nivel);
      pontuacao        - quantidade de inimigos derrotados;
      wave_atual       - número da horda atual (apenas o número é exibido);
      tempo_restante   - tempo restante para a fase atual (horda ou descanso);
      cooldown_restante- tempo que falta para o herói poder atacar novamente;
      wave_ativa       - booleano que indica se a horda está ativa (True) ou se está em período de descanso (False).
    """
    global habilidade_disponivel, proximo_trigger

    largura_hud = 300
    altura_hud = 100
    margem = 20

    # ---- Vida do Herói (Canto Superior Esquerdo) ----
    hud_vida = pygame.Surface((largura_hud, altura_hud), pygame.SRCALPHA)
    pygame.draw.rect(hud_vida, (0, 0, 0, 40), (0, 0, largura_hud - 40, altura_hud - 30), border_radius=20)
    texto_vida_str = f"Vida: {heroi.vida_atual}/{heroi.vida_maxima}"
    texto_vida = FONTE_MODERNA.render(texto_vida_str, True, COR_BRANCO)
    hud_vida.blit(texto_vida, (10, 10))
    largura_barra_vida = 200
    altura_barra_vida = 14
    pos_barra_vida = (10, 40)
    porcentagem_vida = heroi.vida_atual / heroi.vida_maxima if heroi.vida_maxima > 0 else 0
    desenhar_barra_arredondada(hud_vida, pos_barra_vida, largura_barra_vida, altura_barra_vida, 8, (150, 0, 0, 200))
    desenhar_barra_arredondada(hud_vida, pos_barra_vida, int(largura_barra_vida * porcentagem_vida), altura_barra_vida, 8, (0, 200, 0, 200))
    
    # Adiciona os status do herói: Força e Velocidade (abaixo da barra de vida)
    texto_forca = FONTE_MODERNA.render(f"Força: {heroi.ataque}", True, COR_BRANCO)
    hud_vida.blit(texto_forca, (10, 60))
    texto_velocidade = FONTE_MODERNA.render(f"Velocidade: {heroi.velocidade}", True, COR_BRANCO)
    hud_vida.blit(texto_velocidade, (10, 80))
    
    tela.blit(hud_vida, (margem, margem))

    # ---- XP e Nível (Canto Superior Direito) ----
    hud_xp = pygame.Surface((largura_hud, altura_hud), pygame.SRCALPHA)
    pygame.draw.rect(hud_xp, (0, 0, 0, 40), (0, 0, largura_hud - 30, altura_hud - 30), border_radius=20)
    texto_xp_str = f"XP: {heroi.xp_atual}/{heroi.xp_para_proximo_nivel}  |  Nível: {heroi.nivel}"
    texto_xp = FONTE_MODERNA.render(texto_xp_str, True, COR_BRANCO)
    hud_xp.blit(texto_xp, (10, 10))
    largura_barra_xp = 200
    altura_barra_xp = 10
    pos_barra_xp = (10, 40)
    porcentagem_xp = (heroi.xp_atual / heroi.xp_para_proximo_nivel) * 100
    desenhar_barra_arredondada(hud_xp, pos_barra_xp, largura_barra_xp, altura_barra_xp, 6, (0, 0, 150, 150))
    desenhar_barra_arredondada(hud_xp, pos_barra_xp, int(largura_barra_xp * (porcentagem_xp / 100)), altura_barra_xp, 6, (0, 0, 255, 200))
    tela.blit(hud_xp, (LARGURA_TELA - largura_hud - margem, margem))

     # ---- Pontuação, Status do Monstro e Horda (Canto Inferior Esquerdo) ----

    vida_monstro = 30 + (10 * wave_atual)
    ataque_monstro = 5 + (3 * wave_atual)
    velocidade_monstro = 1.5

    # ---- Pontuação, Status do Monstro e Horda (Canto Inferior Esquerdo) ----
    nova_altura_pontuacao = altura_hud + 30
    nova_largura_pontuacao = largura_hud + 200  # aumenta a largura para 100 pixels a mais

    hud_pontuacao = pygame.Surface((nova_largura_pontuacao, nova_altura_pontuacao), pygame.SRCALPHA)
    pygame.draw.rect(hud_pontuacao, (0, 0, 0, 40), (0, 0, nova_largura_pontuacao, nova_altura_pontuacao ), border_radius=20)

    # Exibe os status do monstro (acima do "Inimigos derrotados:")
    texto_monstro_str = f"Monstro - Vida: {vida_monstro} Ataque: {ataque_monstro} Velocidade: {velocidade_monstro:.1f}"
    texto_monstro = FONTE_MODERNA.render(texto_monstro_str, True, COR_BRANCO)
    hud_pontuacao.blit(texto_monstro, (10, 10))

    # Exibe a pontuação e a horda
    texto_pontuacao_str = f"Inimigos derrotados: {pontuacao}"
    texto_pontuacao = FONTE_MODERNA.render(texto_pontuacao_str, True, COR_BRANCO)
    hud_pontuacao.blit(texto_pontuacao, (10, 40))
    texto_horda = FONTE_MODERNA.render(f"Horda: {wave_atual}", True, COR_BRANCO)
    hud_pontuacao.blit(texto_horda, (10, 70))

    tela.blit(hud_pontuacao, (margem, ALTURA_TELA - nova_altura_pontuacao - margem))

    # ---- Tempo Restante e Cooldown (Canto Inferior Direito) ----
    hud_tempo = pygame.Surface((largura_hud, altura_hud), pygame.SRCALPHA)
    pygame.draw.rect(hud_tempo, (0, 0, 0, 40), (0, 0, largura_hud - 30, altura_hud + 10), border_radius=20)

    if (heroi.contador_especial >= heroi.max_contador_especial) and heroi.habilidade_especial_disponivel:
        texto_aviso_especial = FONTE_MODERNA.render("Ataque Especial! (SPACE)", True, COR_VERDE)
    else:
        texto_aviso_especial = FONTE_MODERNA.render(
        f"Especial: {heroi.contador_especial}/{heroi.max_contador_especial}", True, COR_VERMELHO)
    hud_tempo.blit(texto_aviso_especial, (10, 12))
    tempo_restante_int = int(tempo_restante)
    # Se a horda estiver ativa, mostra o tempo da horda; caso contrário, exibe o tempo de descanso.
    if wave_ativa:
        texto_tempo_str = f"Tempo da Horda: {tempo_restante_int}s"
    else:
        texto_tempo_str = f"Descanso: {tempo_restante_int}s"
    texto_tempo_wave = FONTE_MODERNA.render(texto_tempo_str, True, COR_BRANCO)
    hud_tempo.blit(texto_tempo_wave, (10, 40))
    texto_cooldown_str = f"Ataque em: {round(cooldown_restante, 2)}s"
    texto_cooldown = FONTE_MODERNA.render(texto_cooldown_str, True, COR_BRANCO)
    hud_tempo.blit(texto_cooldown, (10, 65))
    tela.blit(hud_tempo, (LARGURA_TELA - largura_hud - margem, ALTURA_TELA - altura_hud - margem))

def ativar_ataque_especial(pontuacao_atual):
    """
    Função a ser chamada quando o ataque especial é ativado.
    Reseta o aviso para voltar a exibir "Carregando!" e atualiza o próximo patamar
    para que o aviso especial volte somente após mais 50 pontos.
    """
    global habilidade_disponivel, proximo_trigger
    habilidade_disponivel = False
    proximo_trigger = pontuacao_atual + 50

def desenhar_barra_arredondada(surface, pos, largura, altura, raio, cor_rgba):
    """
    Desenha uma barra arredondada (retângulo com cantos circulares) na 'surface'.
    
    Parâmetros:
      surface  - a Surface onde a barra será desenhada;
      pos      - tupla (x, y) com a posição superior esquerda;
      largura  - largura da barra;
      altura   - altura da barra;
      raio     - raio para os cantos arredondados;
      cor_rgba - cor no formato (R, G, B, A).
    """
    x, y = pos
    shape_surf = pygame.Surface((largura, altura), pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, cor_rgba, (0, raio, largura, altura - 2*raio))
    pygame.draw.rect(shape_surf, cor_rgba, (raio, 0, largura - 2*raio, altura))
    pygame.draw.circle(shape_surf, cor_rgba, (raio, raio), raio)
    pygame.draw.circle(shape_surf, cor_rgba, (largura - raio, raio), raio)
    pygame.draw.circle(shape_surf, cor_rgba, (raio, altura - raio), raio)
    pygame.draw.circle(shape_surf, cor_rgba, (largura - raio, altura - raio), raio)
    surface.blit(shape_surf, (x, y))
