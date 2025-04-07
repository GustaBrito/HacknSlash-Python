# -*- coding: utf-8 -*-
import pygame
import sys
import random
import os
import json
from datetime import datetime

from configuracoes import (
    LARGURA_TELA,
    ALTURA_TELA,
    COR_PRETO,
    COR_BRANCO,
    COR_AMARELO,
    COR_VERDE,
    COR_BOTAO_SELECIONADO,
    COR_BOTAO_NORMAL,
    FPS,
    TAMANHO_CURSOR,
    ITEM_CURA,
    ITEM_XP,
    TEMPO_EFEITO_DANO,
    EVOLUCAO_FORCA,
    EVOLUCAO_VIDA,
    EVOLUCAO_VELOCIDADE,
    TEXTO_MENU_TITULO,
    TEXTO_MENU_INICIAR,
    TEXTO_MENU_SAIR,
    TEXTO_GAME_OVER,
    TEXTO_TEMPO_SOBREVIVIDO,
    TEXTO_WAVE_ALCANCADA,
    TEXTO_NIVEL_MAXIMO,
    TEXTO_VOLTAR_MENU,
    TEXTO_SAIR_JOGO,
    TEMPO_RECARGA_GOLPE_ESPECIAL,
    COR_BOTAO_FUNDO,
    COR_BOTAO_TEXTO,
    COR_BOTAO_HOVER,
    COR_BOTAO_SELECIONADO
)
from funcoes import (resource_path, carregar_imagem, desenhar_fundo_animado, colisao_corte_monstro, get_save_path)
from jogador import HeroiAnimado
from monstro import MonstroAnimado
from hud import desenhar_hud, ativar_ataque_especial
from waves import GerenciadorWaves

# --------------------- Funções de Leaderboard ---------------------
LEADERBOARD_FILE = get_save_path("leaderboard.json")

def ler_leaderboard():
    import json, os
    
    # Se o arquivo não existir, retornamos lista vazia de cara
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    
    try:
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)  # Se o arquivo estiver vazio ou corrompido, gera exceção
            
            # Se não for lista, retorne lista vazia
            if not isinstance(data, list):
                return []
            
            # Retorna ordenado decrescentemente por pontuação
            return sorted(data, key=lambda x: x.get("pontuacao", 0), reverse=True)
    except Exception as e:
        # Se acontecer qualquer erro (arquivo corrompido, JSON inválido etc.), imprimimos e retornamos []
        print(f"Erro ao ler leaderboard: {e}")
        return []

from datetime import datetime

def salvar_score(record):
    try:
        leaderboard = ler_leaderboard()
        default_record = {
            "nome": "Anonimo",
            "pontuacao": 0,
            "tempo_sobrevivido": 0,
            "wave_maxima": 0,
            "nivel_maximo": 0,
            "data": None
        }
        merged_record = {**default_record, **record}
        merged_record["data"] = datetime.now().strftime("%d/%m/%Y")
        leaderboard.append(merged_record)
        leaderboard.sort(key=lambda x: x.get("pontuacao", 0), reverse=True)
        leaderboard = leaderboard[:10]
        with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
            json.dump(leaderboard, f, indent=4)
        return True
    except Exception as e:
        print(f"Erro ao salvar score: {e}")
        return False

def desenhar_leaderboard(tela, fonte):
    # Carrega a imagem de fundo e redimensiona para a tela inteira
    fundo_leaderboard = carregar_imagem("assets/Menu/Menu_5.png")
    fundo_leaderboard = pygame.transform.scale(fundo_leaderboard, (LARGURA_TELA, ALTURA_TELA))
    tela.blit(fundo_leaderboard, (0, 0))

    # Cria uma fonte maior para o título
    fonte_titulo = pygame.font.Font(resource_path("assets/fonts/Bitwise.ttf"), 45)

    # Título centralizado
    titulo = fonte_titulo.render("LEADERBOARD", True, COR_AMARELO)
    titulo_rect = titulo.get_rect(center=(LARGURA_TELA // 2, 215))
    tela.blit(titulo, titulo_rect)

    # 1) Carrega a imagem do troféu e, se quiser, redimensiona
    trofeu_img = pygame.image.load(resource_path("assets/Menu/trofeu_1.png")).convert_alpha()
    trofeu_img = pygame.transform.scale(trofeu_img, (32, 32))  # Ajuste o tamanho conforme preferir

    # Lê o leaderboard e seleciona top 10
    records = ler_leaderboard()
    top_10 = records[:10]

    # Desenha o cabeçalho das colunas
    cabecalho_text = "NOME        PONTUAÇÃO        DATA"
    cabecalho_surf = fonte.render(cabecalho_text, True, COR_AMARELO)
    cabecalho_rect = cabecalho_surf.get_rect(center=(LARGURA_TELA // 2, 270))
    tela.blit(cabecalho_surf, cabecalho_rect)

    y_inicial = 310
    espacamento_linha = 35
    y = y_inicial

    for i, record in enumerate(top_10):
        nome = record.get("nome", "Anonimo")
        pontuacao = record.get("pontuacao", 0)
        data = record.get("data", "--/--/----")

        # 2) Define quantos troféus desenhar dependendo da posição
        if i == 0:
            num_trofeus = 3
        elif i == 1:
            num_trofeus = 2
        elif i == 2:
            num_trofeus = 1
        else:
            num_trofeus = 0

        # Desenha o texto da linha (sem estrelas agora, apenas nome - pontuação - data)
        texto_linha = f"{nome:<12} {pontuacao:>8}     {data}"
        linha_surface = fonte.render(texto_linha, True, COR_AMARELO)

        # Definimos a posição do texto:
        linha_rect = linha_surface.get_rect(center=(LARGURA_TELA // 2, y))
        tela.blit(linha_surface, linha_rect)

        # 3) Desenha os troféus ao lado (por exemplo, à esquerda do texto)
        # Defina um espaçamento horizontal entre os troféus
        espaco_trofeu = 35

        for t in range(num_trofeus):
            # O x do primeiro troféu ficará à esquerda do texto,
            # cada troféu adicional fica ainda mais à esquerda
            trofeu_x = linha_rect.left - (trofeu_img.get_width() + 5) - (t * espaco_trofeu)
            trofeu_y = linha_rect.centery - trofeu_img.get_height() // 2
            
            tela.blit(trofeu_img, (trofeu_x, trofeu_y))

        # Atualiza a posição vertical para a próxima linha
        y += espacamento_linha

    # Botão "Voltar" centralizado no rodapé
    COR_AZUL_MARINHO = (0, 51, 102)
    COR_AZUL_MARINHO_HOVER = (0, 76, 153)
    
    pos_mouse = pygame.mouse.get_pos()
    botao_rect = pygame.Rect(LARGURA_TELA // 2 - 100, ALTURA_TELA - 100, 200, 50)
    
    # Define a cor do botão (hover ou normal)
    cor_botao = COR_AZUL_MARINHO
    if botao_rect.collidepoint(pos_mouse):
        cor_botao = COR_AZUL_MARINHO_HOVER

    pygame.draw.rect(tela, cor_botao, botao_rect, border_radius=10)
    
    texto_botao = fonte.render("Voltar", True, COR_BRANCO)
    tela.blit(
        texto_botao,
        (botao_rect.centerx - texto_botao.get_width() // 2,
         botao_rect.centery - texto_botao.get_height() // 2)
    )

    return botao_rect

# ------------------------------------------------------------------

def desenhar_menu(tela, fonte, estado_menu):
    """
    Desenha o menu inicial na tela com botões estilizados e imagem de fundo.
    """
    # Desenha a imagem de fundo
    menu_fundo = carregar_imagem("assets/menu/menu_1.png")
    tela.blit(menu_fundo, (0, 0))

    # Define cores para os botões
    COR_AZUL_MARINHO = (0, 51, 102)  # Azul marinho
    COR_AZUL_MARINHO_HOVER = (0, 76, 153)  # Azul marinho mais claro para o efeito hover
    COR_TEXTO_BOTAO = COR_BRANCO  # Texto branco

    # Opções do menu
    opcoes = [TEXTO_MENU_INICIAR, "PLACAR", TEXTO_MENU_SAIR]
    y_pos = 400
    for i, opcao in enumerate(opcoes):
        cor_fundo = COR_AZUL_MARINHO
        pos_mouse = pygame.mouse.get_pos()
        texto = fonte.render(opcao, True, COR_TEXTO_BOTAO)
        botao_rect = pygame.Rect(LARGURA_TELA // 2 - 100, y_pos + i * 60, 200, 50)
        if botao_rect.collidepoint(pos_mouse):
            cor_fundo = COR_AZUL_MARINHO_HOVER
        pygame.draw.rect(tela, cor_fundo, botao_rect, border_radius=10)
        tela.blit(texto, (botao_rect.centerx - texto.get_width() // 2, botao_rect.centery - texto.get_height() // 2))
    # (O estado_menu pode ser usado para efeitos visuais extras)

def desenhar_tela_pausa(tela, fonte):
    """
    Desenha a tela de pausa com uma imagem de fundo e botões estilizados.
    Retorna uma lista de retângulos dos botões para verificação de cliques.
    """
    # Carrega a imagem de fundo
    fundo_pausa = carregar_imagem("assets/Menu/Menu_3.png")
    fundo_pausa = pygame.transform.scale(fundo_pausa, (LARGURA_TELA, ALTURA_TELA))  # Redimensiona para o tamanho da tela
    tela.blit(fundo_pausa, (0, 0))  # Desenha a imagem de fundo

    # Define cores para os botões
    COR_AZUL_MARINHO = (0, 51, 102)  # Azul marinho
    COR_AZUL_MARINHO_HOVER = (0, 76, 153)  # Azul marinho mais claro para o efeito hover
    COR_TEXTO_BOTAO = COR_BRANCO  # Texto branco

    # Opções do menu de pausa
    opcoes = ["Continuar", "Menu Principal", "Sair"]  # Texto atualizado
    botoes_pausa = []  # Armazenará os retângulos dos botões para verificar cliques
    y_pos = 400  # Posição vertical inicial dos botões

    for i, opcao in enumerate(opcoes):
        # Cria o retângulo do botão
        botao_rect = pygame.Rect(LARGURA_TELA // 2 - 100, y_pos + i * 80, 200, 50)
        botoes_pausa.append(botao_rect)  # Adiciona à lista de retângulos

        # Verifica se o mouse está sobre o botão
        pos_mouse = pygame.mouse.get_pos()
        cor_botao = COR_AZUL_MARINHO_HOVER if botao_rect.collidepoint(pos_mouse) else COR_AZUL_MARINHO

        # Desenha o botão
        pygame.draw.rect(tela, cor_botao, botao_rect, border_radius=10)  # Bordas arredondadas
        texto = fonte.render(opcao, True, COR_TEXTO_BOTAO)
        tela.blit(texto, (botao_rect.centerx - texto.get_width() // 2, botao_rect.centery - texto.get_height() // 2))

    return botoes_pausa

def verificar_drop(monstro):
    """
    Verifica se o monstro deve dropar um item ao morrer.
    Retorna o item ou None se não dropar nada.
    """
    if random.random() <= ITEM_CURA["chance"]:
        return ITEM_CURA
    return ITEM_XP  # Sempre dropa XP

def aplicar_efeito_dano(imagem, tempo_efeito_dano):
    """
    Aplica um efeito vermelho temporário na imagem.
    """
    if pygame.time.get_ticks() - tempo_efeito_dano < TEMPO_EFEITO_DANO:
        vermelho = pygame.Surface(imagem.get_size(), pygame.SRCALPHA)
        vermelho.fill((255, 0, 0, 200))  # Vermelho com 80% de opacidade
        imagem.blit(vermelho, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return imagem

def exibir_opcoes_evolucao(tela, fonte):
    """
    Exibe a tela de evolução (somente o fundo) e retorna a escolha do jogador.
    "1" adiciona vida, "2" adiciona força e "3" adiciona velocidade.
    """
    fundo_evolucao = carregar_imagem("assets/Menu/Menu_4.png")
    fundo_evolucao = pygame.transform.scale(fundo_evolucao, (LARGURA_TELA, ALTURA_TELA))
    tela.blit(fundo_evolucao, (0, 0))
    pygame.display.flip()

    # Captura a escolha do jogador
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Tecla 1 para VIDA
                    return "vida"
                elif event.key == pygame.K_2:  # Tecla 2 para FORÇA
                    return "forca"
                elif event.key == pygame.K_3:  # Tecla 3 para VELOCIDADE
                    return "velocidade"

def desenhar_game_over(tela, fonte, tempo_sobrevivido, wave_maxima, nivel_maximo, player_name):
    """
    Desenha a tela de game over com uma imagem de fundo e botões modernos.
    """
    # Carrega a imagem de fundo
    fundo_game_over = carregar_imagem("assets/Menu/Menu_2.png")
    fundo_game_over = pygame.transform.scale(fundo_game_over, (LARGURA_TELA, ALTURA_TELA))  # Redimensiona para o tamanho da tela
    tela.blit(fundo_game_over, (0, 0))  # Desenha a imagem de fundo

    # Define cores para os botões
    COR_AZUL_MARINHO = (0, 51, 102)  # Azul marinho
    COR_AZUL_MARINHO_HOVER = (0, 76, 153)  # Azul marinho mais claro para o efeito hover
    COR_TEXTO_BOTAO = COR_BRANCO  # Texto branco

    tempo_sobrevivido = tempo_sobrevivido if tempo_sobrevivido is not None else 0
    wave_maxima = wave_maxima if wave_maxima is not None else 0
    nivel_maximo = nivel_maximo if nivel_maximo is not None else 0

    # Informações da partida
    info_tempo = fonte.render(TEXTO_TEMPO_SOBREVIVIDO.format(tempo_sobrevivido), True, COR_BRANCO)
    tela.blit(info_tempo, (LARGURA_TELA // 2 - info_tempo.get_width() // 2, 325))

    info_wave = fonte.render(TEXTO_WAVE_ALCANCADA.format(wave_maxima), True, COR_BRANCO)
    tela.blit(info_wave, (LARGURA_TELA // 2 - info_wave.get_width() // 2, 375))

    info_nivel = fonte.render(TEXTO_NIVEL_MAXIMO.format(nivel_maximo), True, COR_BRANCO)
    tela.blit(info_nivel, (LARGURA_TELA // 2 - info_nivel.get_width() // 2, 425))

    # Desenha o input para o nome do jogador
    input_text = fonte.render("Digite seu nome para salvar: " + player_name, True, COR_VERDE)
    tela.blit(input_text, (LARGURA_TELA // 2 - input_text.get_width() // 2, 275))

    # Opções do menu (botões)
    opcoes = [TEXTO_VOLTAR_MENU, TEXTO_SAIR_JOGO]
    botoes_rect = []  # Armazena os retângulos dos botões para verificar cliques
    y_pos = 500
    for i, opcao in enumerate(opcoes):
        botao_rect = pygame.Rect(LARGURA_TELA // 2 - 100, y_pos + i * 80, 200, 50)
        botoes_rect.append(botao_rect)
        pos_mouse = pygame.mouse.get_pos()
        cor_botao = COR_AZUL_MARINHO_HOVER if botao_rect.collidepoint(pos_mouse) else COR_AZUL_MARINHO
        pygame.draw.rect(tela, cor_botao, botao_rect, border_radius=10)
        texto = fonte.render(opcao, True, COR_BRANCO)
        tela.blit(texto, (botao_rect.centerx - texto.get_width() // 2, botao_rect.centery - texto.get_height() // 2))
    return botoes_rect

def main():
    # Inicialização do Pygame
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Hack'n'Slash Uninter - Secret wave")
    fonte = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()

    # Carregar recursos
    icone = carregar_imagem("assets/icon.png")
    pygame.display.set_icon(icone)
    imagem_fundo = carregar_imagem("assets/fundo_tile.png")
    mouse_idle = carregar_imagem("assets/Mouse/Idle/idle_1.png")
    mouse_click = carregar_imagem("assets/Mouse/Click/click_1.png")
    mouse_idle = pygame.transform.scale(mouse_idle, TAMANHO_CURSOR)
    mouse_click = pygame.transform.scale(mouse_click, TAMANHO_CURSOR)
    pygame.mouse.set_visible(False)

    # Carregar sons (usando pygame.mixer.Sound)
    som_ataque    = pygame.mixer.Sound(resource_path("assets/Sons/ataque.mp3"))
    som_fire      = pygame.mixer.Sound(resource_path("assets/Sons/fire_ataque.mp3"))
    som_game_over = pygame.mixer.Sound(resource_path("assets/Sons/game_over.mp3"))
    som_level_up  = pygame.mixer.Sound(resource_path("assets/Sons/level_up.mp3"))
    som_start     = pygame.mixer.Sound(resource_path("assets/Sons/start.mp3"))

    # Música de fundo (usando pygame.mixer.music)
    pygame.mixer.music.load(resource_path("assets/Sons/musica_fundo.mp3"))
    pygame.mixer.music.set_volume(0.2)  # Volume baixo
    pygame.mixer.music.play(-1)  # Loop infinito

    # Estados do jogo
    estado_jogo = "menu"
    estado_menu = 0  # 0 = Iniciar, 1 = Sair
    game_over = False

    # Variáveis do jogo
    heroi = None
    lista_monstros = []
    gerenciador = None
    pontuacao = 0
    mouse_atual = mouse_idle
    itens_dropados = []  # Lista para armazenar os itens dropados

    tempo_sobrevivido = 0  # Inicializa com 0
    wave_maxima = 0  # Inicializa com 0
    nivel_maximo = 0  # Inicializa com 0

    # Variáveis para controle da morte
    hero_died = False
    death_time = 0

    player_name = ""
    record_salvo = False

    ultima_tecla_time = 0  
    tecla_processada = False

    def resetar_jogo():
        nonlocal heroi, lista_monstros, gerenciador, pontuacao, itens_dropados, hero_died, death_time, tempo_inicio, player_name, record_salvo
        try:
            heroi = None
            lista_monstros = []
            gerenciador = None
            pontuacao = 0
            itens_dropados = []
            hero_died = False
            death_time = 0
            tempo_inicio = pygame.time.get_ticks() if 'tempo_inicio' not in locals() else 0
            player_name = ""
            record_salvo = False
        except Exception as e:
            print(f"Erro ao resetar jogo: {e}")
            # Valores padrão de fallback
            heroi = None
            lista_monstros = []
            gerenciador = None
            pontuacao = 0

    while True:
        # Captura todos os eventos uma única vez
        eventos = pygame.event.get()

        tecla_processada = False

        for event in eventos:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # ----------------- Menu Principal -----------------

            # Controles do menu
            if estado_jogo == "menu":
                pos_mouse = pygame.mouse.get_pos()
                y_pos = 400
                opcoes = [TEXTO_MENU_INICIAR, "Placar", TEXTO_MENU_SAIR]
                for i, opcao in enumerate(opcoes):
                    botao_rect = pygame.Rect(LARGURA_TELA // 2 - 100, y_pos + i * 60, 200, 50)
                    if botao_rect.collidepoint(pos_mouse):
                        estado_menu = i
                for event in eventos:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for i, opcao in enumerate(opcoes):
                            botao_rect = pygame.Rect(LARGURA_TELA // 2 - 100, y_pos + i * 60, 200, 50)
                            if botao_rect.collidepoint(pos_mouse):
                                if i == 0:  # Iniciar jogo
                                    heroi = HeroiAnimado((LARGURA_TELA//2, ALTURA_TELA//2), 0, 0)
                                    lista_monstros = []
                                    gerenciador = GerenciadorWaves(15, 10)
                                    gerenciador.iniciar_wave()
                                    pontuacao = 0
                                    tempo_inicio = pygame.time.get_ticks()
                                    estado_jogo = "jogando"
                                elif i == 1:  # Placar (Leaderboard)
                                    estado_jogo = "leaderboard"
                                elif i == 2:  # Sair
                                    pygame.quit()
                                    sys.exit()

            # Controles durante o jogo
            elif estado_jogo == "jogando":
                for event in eventos:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_atual = mouse_click
                        som_ataque.play()
                        heroi.iniciar_ataque(pygame.mouse.get_pos())
                    elif event.type == pygame.MOUSEBUTTONUP:
                        mouse_atual = mouse_idle
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            if heroi.habilidade_especial_disponivel:
                                heroi.ativar_habilidade_especial()
                                som_fire.play()
                                ativar_ataque_especial(pontuacao)
                        elif event.key == pygame.K_ESCAPE:  # Pausa o jogo ao pressionar ESC
                            estado_jogo = "pausado"

            # Controles durante o jogo pausado
            elif estado_jogo == "pausado":
                botoes_pausa = desenhar_tela_pausa(tela, fonte)  # Desenha a tela de pausa e obtém os retângulos dos botões

                for event in eventos:
                    if event.type == pygame.MOUSEBUTTONDOWN:  # Verifica se o mouse foi clicado
                        pos_mouse = pygame.mouse.get_pos()  # Obtém a posição do mouse

                        # Verifica qual botão foi clicado
                        for i, botao_rect in enumerate(botoes_pausa):
                            if botao_rect.collidepoint(pos_mouse):  # Se o clique foi dentro do retângulo do botão
                                if i == 0:  # Botão "Continuar"
                                    estado_jogo = "jogando"  # Volta ao jogo
                                elif i == 1:  # Botão "Menu Principal"
                                    resetar_jogo()
                                    estado_jogo = "menu"  # Volta ao menu principal
                                elif i == 2:  # Botão "Sair"
                                    # Chama a função de game over com os valores atuais
                                    tempo_sobrevivido = (pygame.time.get_ticks() - tempo_inicio) // 1000
                                    wave_maxima = gerenciador.wave_atual if gerenciador else 0
                                    nivel_maximo = heroi.nivel if heroi else 0
                                    estado_jogo = "game_over"  # Muda para a tela de game over

            elif estado_jogo == "game_over":
                botoes_rect = desenhar_game_over(tela, fonte, tempo_sobrevivido, wave_maxima, nivel_maximo, player_name)
                
                for event in eventos:
                    agora = pygame.time.get_ticks()
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos_mouse = pygame.mouse.get_pos()
                        for i, botao_rect in enumerate(botoes_rect):
                            if botao_rect.collidepoint(pos_mouse):
                                # Salvamento ao clicar nos botões
                                if player_name.strip() and not record_salvo:
                                    record = {
                                        "nome": player_name.strip(),
                                        "tempo_sobrevivido": tempo_sobrevivido,
                                        "wave_maxima": wave_maxima,
                                        "nivel_maximo": nivel_maximo,
                                        "pontuacao": pontuacao
                                    }
                                    record_salvo = salvar_score(record)
                                
                                # Ações dos botões
                                if i == 0:  # Voltar ao menu
                                    resetar_jogo()
                                    estado_jogo = "menu"
                                elif i == 1:  # Sair do jogo
                                    pygame.quit()
                                    sys.exit()
                    
                    # Sistema de input com debounce
                    elif event.type == pygame.TEXTINPUT and not tecla_processada and (agora - ultima_tecla_time) > 50:
                        if len(player_name) < 20 and event.text.strip():
                            player_name += event.text
                            tecla_processada = True
                            ultima_tecla_time = agora
                            
                    elif event.type == pygame.KEYDOWN and not tecla_processada and (agora - ultima_tecla_time) > 50:
                        if event.key == pygame.K_BACKSPACE:
                            player_name = player_name[:-1]
                            tecla_processada = True
                            ultima_tecla_time = agora
                            
                        elif event.key == pygame.K_RETURN and player_name.strip() and not record_salvo:
                            record = {
                                "nome": player_name.strip(),
                                "tempo_sobrevivido": tempo_sobrevivido,
                                "wave_maxima": wave_maxima,
                                "nivel_maximo": nivel_maximo,
                                "pontuacao": pontuacao
                            }
                            record_salvo = salvar_score(record)
                            tecla_processada = True
                            ultima_tecla_time = agora

                # Reset da flag de processamento para o próximo frame
                tecla_processada = False

            # ----------------- Tela de Leaderboard -----------------
            elif estado_jogo == "leaderboard":
                for event in eventos:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos_mouse = pygame.mouse.get_pos()
                        botao_voltar = desenhar_leaderboard(tela, fonte)  # Obtem o retângulo do botão "Voltar"
                        if botao_voltar.collidepoint(pos_mouse):
                            estado_jogo = "menu"

        # Lógica do jogo
        if estado_jogo == "jogando":
            # Captura as teclas pressionadas
            teclas = pygame.key.get_pressed()
            heroi.mover(teclas)  # Move o herói com base nas teclas pressionadas

            # Atualizar herói
            heroi.update()

            # Verificar morte do herói
            if heroi.vida_atual <= 0 and not hero_died:
                hero_died = True
                death_time = pygame.time.get_ticks()
                heroi.estado = "dead"  # Ativa a animação de morte
                som_game_over.play()

            # Se o herói morreu, atualiza a animação de morte e aguarda 2 segundos
            if hero_died:
                heroi.update()  # Atualiza para avançar a animação de morte
                if pygame.time.get_ticks() - death_time >= 1500:
                    estado_jogo = "game_over"
                    tempo_sobrevivido = (death_time - tempo_inicio) // 1000
                    wave_maxima = gerenciador.wave_atual if gerenciador else 0
                    nivel_maximo = heroi.nivel if heroi else 0    

            if heroi.em_evolucao:
                escolha = exibir_opcoes_evolucao(tela, fonte)
                if escolha == "vida":
                    heroi.aumentar_vida()
                    som_level_up.play()
                elif escolha == "forca":
                    heroi.aumentar_forca()
                    som_level_up.play()
                elif escolha == "velocidade":
                    heroi.aumentar_velocidade()
                    som_level_up.play()
                heroi.em_evolucao = False  # Desativa o estado de evolução


            # Atualizar e desenhar o efeito de fogo da habilidade especial
            if heroi.habilidade_especial_ativa:
                heroi.efeito_fogo.atualizar()
                for monstro in lista_monstros[:]:  # Usamos [:] para iterar sobre uma cópia da lista
                    monstro.receber_golpe_especial()  # Mata o monstro instantaneamente
                    pontuacao += 1  # Incrementa a pontuação
                    heroi.adicionar_contador_especial(1)
                    item_dropado = monstro.drop_item()
                    if item_dropado:
                        itens_dropados.append(item_dropado)
                    lista_monstros.remove(monstro)

            # Verificar colisões de ataque
            cooldown_restante = 0
            if heroi.estado != 'dead' and heroi.atacando:
                cooldown_restante = max((heroi.duracao_ataque - (pygame.time.get_ticks() - heroi.tempo_ataque)) / 1000, 0)
                for monstro in lista_monstros:
                    if monstro.esta_vivo() and colisao_corte_monstro(heroi.rect_corte, monstro.rect):
                        monstro.receber_dano(heroi.ataque)

            # Atualiza e processa cada monstro
            for monstro in lista_monstros[:]:
                # Chama o update para processar a animação e o fade-out
                resultado = monstro.update(tela)
                if resultado is not False:
                    # Fade-out completo: remove o monstro e trata o item dropado
                    pontuacao += 1
                    heroi.adicionar_contador_especial(1)
                    if resultado:
                        itens_dropados.append(resultado)
                    lista_monstros.remove(monstro)
                else:
                    # Se o monstro ainda não terminou o fade-out, atualiza seu movimento e posição
                    alvo_x = heroi.rect_heroi.centerx + heroi.camera_x
                    alvo_y = heroi.rect_heroi.centery + heroi.camera_y
                    monstro.mover_em_direcao(alvo_x, alvo_y)
                    monstro.atualizar_rect(heroi.camera_x, heroi.camera_y)
                    # Se o monstro não estiver no estado de morte, ele pode causar dano
                    if monstro.estado != 'dying' and monstro.rect.colliderect(heroi.rect_heroi):
                        heroi.receber_dano(monstro.ataque)

            # Atualizar waves
            if gerenciador:
                gerenciador.atualizar(heroi, lista_monstros, LARGURA_TELA, ALTURA_TELA)
                
            # Atualizar waves
            if gerenciador:
                gerenciador.atualizar(heroi, lista_monstros, LARGURA_TELA, ALTURA_TELA)
                if gerenciador.wave_em_andamento:
                    tempo_exibicao = int(gerenciador.tempo_restante_wave())
                else:
                    # Calcula o tempo restante de descanso
                    tempo_descanso_restante = gerenciador.tempo_descanso - (pygame.time.get_ticks()/1000 - gerenciador.tempo_inicio_descanso)
                    tempo_exibicao = int(max(tempo_descanso_restante, 0))
            else:
                tempo_exibicao = 0


            for item in itens_dropados[:]:  # Usamos [:] para iterar sobre uma cópia da lista
                # Passa a posição do herói no mundo e o rect do herói
                if item.update(
                    (heroi.rect_heroi.centerx + heroi.camera_x, heroi.rect_heroi.centery + heroi.camera_y),
                    heroi.rect_heroi
                ):
                    if item.tipo == 'vida':
                        heroi.vida_atual = min(heroi.vida_atual + 15, heroi.vida_maxima)  # Adiciona 15 de vida
                    elif item.tipo == 'xp':
                        heroi.ganhar_xp(10)  # Adiciona 10 de XP
                    itens_dropados.remove(item)  # Remove o item da lista após ser coletado

        # Renderização
        tela.fill(COR_PRETO)

        if estado_jogo == "menu":
            desenhar_menu(tela, fonte, estado_menu)
        elif estado_jogo == "jogando":
            # Fundo
            desenhar_fundo_animado(tela, imagem_fundo, heroi.camera_x, heroi.camera_y, LARGURA_TELA, ALTURA_TELA)

            # Monstros
            for monstro in lista_monstros:
                monstro.desenhar(tela)

            # Herói
            heroi.draw(tela)
            heroi.desenhar_corte(tela)

            # Efeito de fogo da habilidade especial
            if heroi.habilidade_especial_ativa:
                heroi.efeito_fogo.desenhar(tela)

            # Itens dropados
            for item in itens_dropados:
                item.draw(tela, heroi.camera_x, heroi.camera_y)

            # HUD
            desenhar_hud(tela, heroi, pontuacao,
             gerenciador.wave_atual, 
             tempo_exibicao, 
             cooldown_restante,
             gerenciador.wave_em_andamento)

        elif estado_jogo == "pausado":
            botoes_pausa = desenhar_tela_pausa(tela, fonte)
        elif estado_jogo == "game_over":
            botoes_rect = desenhar_game_over(tela, fonte, tempo_sobrevivido, wave_maxima, nivel_maximo, player_name)
        elif estado_jogo == "leaderboard":
            desenhar_leaderboard(tela, fonte)

        # Cursor
        pos_mouse = pygame.mouse.get_pos()
        tela.blit(mouse_atual, pos_mouse)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
