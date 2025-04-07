# heroi.py (Exemplo de classe animada)

import pygame
import os
import math
import random
from funcoes import (resource_path, carregar_imagem)
from configuracoes import (
    TEMPO_INVENCIBILIDADE,
    TEMPO_EFEITO_DANO,
    TAMANHO_SPRITE_HEROI,
    TAMANHO_SPRITE_CORTE,
    LARGURA_TELA,
    ALTURA_TELA
)

def carregar_frames(pasta, prefixo, quantidade, largura=None, altura=None):
    frames = []
    for i in range(1, quantidade + 1):
        nome_arquivo = f"{prefixo}_{i}.png"
        caminho_completo = os.path.join(pasta, nome_arquivo)
        imagem = carregar_imagem(caminho_completo)
        if largura and altura:
            imagem = pygame.transform.scale(imagem, (largura, altura))
        frames.append(imagem)
    return frames

class EfeitoFogo:
    def __init__(self, posicao, raio_maximo):
        self.frames = carregar_frames("assets/Fogo", "Fogo", 12)
        self.posicao = posicao
        self.raio_maximo = raio_maximo
        self.raio_atual = 0
        self.frame_atual = 0
        self.tempo_ultimo_frame = pygame.time.get_ticks()
        self.tempo_por_frame = 100
        self.ativo = False
        self.particulas = []
        self.tempo_inicio_expansao = 0  # Tempo em que a expansão começou

    def iniciar(self):
        self.raio_atual = 0
        self.ativo = True
        self.tempo_inicio_expansao = pygame.time.get_ticks()  # Registra o início da expansão
        self.particulas = self._criar_particulas()

    def _criar_particulas(self):
        particulas = []
        num_particulas = 70
        for _ in range(num_particulas):
            # Gera um ângulo aleatório entre 0 e 360 graus
            angulo = math.radians(random.uniform(0, 360))
            # Gera um raio inicial aleatório (começando de 0)
            raio_inicial = 0
            # Gera um deslocamento aleatório para a posição
            offset_x = random.uniform(-10, 10)
            offset_y = random.uniform(-10, 10)
            # Gera um tamanho aleatório para a partícula
            tamanho = random.uniform(0.8, 1.5)
            # Armazena os dados da partícula
            particulas.append({
                "angulo": angulo,
                "raio_inicial": raio_inicial,
                "offset_x": offset_x,
                "offset_y": offset_y,
                "tamanho": tamanho,
                "frame": random.randint(0, len(self.frames) - 1)
            })
        return particulas

    def atualizar(self):
        if not self.ativo:
            return

        # Calcula o tempo decorrido desde o início da expansão
        tempo_decorrido = pygame.time.get_ticks() - self.tempo_inicio_expansao

        # Atualiza o raio do efeito com base no tempo decorrido
        self.raio_atual = min(tempo_decorrido * 0.3, self.raio_maximo)  # Ajuste a velocidade conforme necessário

        # Atualiza a animação do fogo
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.tempo_ultimo_frame > self.tempo_por_frame:
            self.frame_atual = (self.frame_atual + 1) % len(self.frames)
            self.tempo_ultimo_frame = tempo_atual

        # Atualiza as partículas de fogo para seguir o crescimento do círculo
        for particula in self.particulas:
            # Ajusta o raio da partícula com base no tempo decorrido
            particula["raio_inicial"] = self.raio_atual

        # Desativa o efeito quando o raio atinge o máximo
        if self.raio_atual >= self.raio_maximo:
            self.ativo = False

    def desenhar(self, tela):
        if not self.ativo:
            return

        # Desenha o círculo de fogo
        superficie_transparente = pygame.Surface((self.raio_atual * 2, self.raio_atual * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            superficie_transparente,
            (255, 100, 0, 100),  # Cor laranja com transparência
            (self.raio_atual, self.raio_atual),
            self.raio_atual
        )
        tela.blit(superficie_transparente, (self.posicao[0] - self.raio_atual, self.posicao[1] - self.raio_atual))

        # Desenha as partículas de fogo ao redor do círculo
        for particula in self.particulas:
            # Calcula a posição da partícula com base no ângulo e no raio atual
            x = self.posicao[0] + math.cos(particula["angulo"]) * particula["raio_inicial"] + particula["offset_x"]
            y = self.posicao[1] + math.sin(particula["angulo"]) * particula["raio_inicial"] + particula["offset_y"]
            # Obtém o frame da partícula
            frame = self.frames[particula["frame"]]
            # Redimensiona o frame com base no tamanho da partícula
            frame = pygame.transform.scale(frame, (int(frame.get_width() * particula["tamanho"]), int(frame.get_height() * particula["tamanho"])))
            # Desenha a partícula na tela
            tela.blit(frame, (x - frame.get_width() // 2, y - frame.get_height() // 2))

class HeroiAnimado:
    def __init__(self, posicao_inicial, camera_x=0, camera_y=0):
        # Atributos de câmera e posição
        self.rect_heroi = pygame.Rect(0, 0, 64, 64)  # tamanho padrão, ajustado depois
        self.rect_heroi.center = posicao_inicial
        self.camera_x = camera_x
        self.camera_y = camera_y

        # Atributos do herói
        self.vida_maxima = 100
        self.vida_atual = 100
        self.xp_atual = 0
        self.nivel = 1
        self.ataque = 20
        self.velocidade = 3

        self.em_evolucao = False

        # Habilidade especial
        self.habilidade_especial_disponivel = False
        self.habilidade_especial_ativa = False
        self.tempo_inicio_habilidade = 0
        self.raio_habilidade = 0
        self.raio_maximo = max(LARGURA_TELA, ALTURA_TELA)
        self.efeito_fogo = EfeitoFogo((LARGURA_TELA // 2, ALTURA_TELA // 2), self.raio_maximo)

        self.xp = 0  # Adiciona um atributo para armazenar a experiência do herói
        self.nivel = 1  # Nível inicial do herói
        self.xp_para_proximo_nivel = 100  # XP necessário para subir de nível

        # Novo: Atributos para o contador da habilidade especial
        self.contador_especial = 0
        self.max_contador_especial = 50

        # Estados
        self.estado = 'idle'   # idle, run, attack, hurt, dead
        self.invencivel = False
        self.tempo_inicial_invencivel = 0

        # Controle de animação
        self.frame_atual = 0
        self.tempo_ultimo_frame = pygame.time.get_ticks()
        self.tempo_por_frame = 50  # ms entre quadros
        self.tempo_efeito_dano = 0  # Tempo inicial do efeito de dano

        # Carregamos as animações (exemplo com quantidades fictícias de frames)
        self.frames_idle = carregar_frames("assets/Heroi/01-Parado", "Parado", 12, TAMANHO_SPRITE_HEROI[0], TAMANHO_SPRITE_HEROI[1])
        self.frames_run = carregar_frames("assets/Heroi/02-Corrida", "Corrida", 10, TAMANHO_SPRITE_HEROI[0], TAMANHO_SPRITE_HEROI[1])
        self.frames_attack = carregar_frames("assets/Heroi/03-Ataque/No_Effect", "Ataque", 8, TAMANHO_SPRITE_HEROI[0], TAMANHO_SPRITE_HEROI[1])
        self.frames_corte = carregar_frames("assets/Efeito_espada", "Corte", 6, TAMANHO_SPRITE_CORTE[0], TAMANHO_SPRITE_CORTE[1])
        self.frames_dano = carregar_frames("assets/Heroi/04-Dano", "Dano", 6, TAMANHO_SPRITE_HEROI[0], TAMANHO_SPRITE_HEROI[1])
        self.frames_morte = carregar_frames("assets/Heroi/05-Morte", "Morte", 8, TAMANHO_SPRITE_HEROI[0], TAMANHO_SPRITE_HEROI[1])

        # Imagem atual (frame atual do estado atual)
        self.imagem_atual = self.frames_idle[0]

        # Lógica de ataque (caso queira manter tempo/duração)
        self.atacando = False
        self.tempo_ataque = 0
        self.duracao_ataque = 250  # ex.: 1/4 segundo de animação de ataque
        self.frame_atual_corte = 0  # Frame atual da animação de corte
        self.angulo_corte = 0  # Ângulo do efeito de corte
        self.rect_corte = pygame.Rect(0, 0, TAMANHO_SPRITE_CORTE[0], TAMANHO_SPRITE_CORTE[1])  # Retângulo do corte

        # Direção do herói (1 para direita, -1 para esquerda)
        self.direcao = 1

    def set_estado(self, novo_estado):
        """Muda o estado do herói e reinicia a animação desse estado."""
        if self.estado == 'dead':
            return  # Não muda de estado se o herói estiver morto

        if novo_estado != self.estado:
            self.estado = novo_estado
            self.frame_atual = 0
            self.tempo_ultimo_frame = pygame.time.get_ticks()
    def adicionar_contador_especial(self, pontos):
        """
        Incrementa o contador da habilidade especial.
        Se atingir 50, ativa a habilidade.
        """
        # Se a habilidade já está ativa, não acumula mais pontos
        if self.habilidade_especial_ativa:
            return

        self.contador_especial += pontos

        # Garante que o contador não ultrapasse o máximo
        if self.contador_especial >= self.max_contador_especial:
            self.contador_especial = self.max_contador_especial
            self.habilidade_especial_disponivel = True

    def mover(self, teclas):
        # Se o herói está no estado de hit ou morto, não altera o estado
        if self.estado in ['hit', 'dead']:
            return

        movimento_x = 0
        movimento_y = 0

        if teclas[pygame.K_w]:
            movimento_y -= self.velocidade
        if teclas[pygame.K_s]:
            movimento_y += self.velocidade
        if teclas[pygame.K_a]:
            movimento_x -= self.velocidade
            self.direcao = 1  # Ajustar para -1 se necessário para a esquerda
        if teclas[pygame.K_d]:
            movimento_x += self.velocidade
            self.direcao = -1  # Ajustar para 1 se necessário para a direita

        if movimento_x == 0 and movimento_y == 0:
            if self.atacando:
                self.set_estado('attack')
            else:
                self.set_estado('idle')

        if movimento_x != 0 and movimento_y != 0:
            movimento_x *= 0.7071
            movimento_y *= 0.7071

        if movimento_x != 0 or movimento_y != 0:
            self.camera_x += movimento_x
            self.camera_y += movimento_y
            if not self.atacando:
                self.set_estado('run')


    def iniciar_ataque(self, mouse_pos):
        """Inicia a animação de ataque (efeito de corte) e define a hitbox do corte."""
        if self.estado == 'dead':
            return  # Não permite ataque se o herói estiver morto

        if not self.atacando:
            self.atacando = True
            self.tempo_ataque = pygame.time.get_ticks()
            # Muda o estado para 'attack' para iniciar a animação de ataque
            self.set_estado('attack')
            # Calcula o ângulo do corte com base na posição do mouse
            self.angulo_corte = math.atan2(mouse_pos[1] - self.rect_heroi.centery, mouse_pos[0] - self.rect_heroi.centerx)
            self.frame_atual_corte = 0  # Reinicia a animação de corte

    def update(self):
        tempo_atual = pygame.time.get_ticks()
        # Atualiza o rect do herói (mantendo-o centralizado)
        self.rect_heroi = self.imagem_atual.get_rect()
        self.rect_heroi.center = (LARGURA_TELA // 2, ALTURA_TELA // 2)
        self.efeito_fogo.posicao = (self.rect_heroi.centerx, self.rect_heroi.centery)

        # Se o herói está morto, trata a animação de morte separadamente
        if self.estado == "dead":
            if tempo_atual - self.tempo_ultimo_frame > self.tempo_por_frame:
                if self.frame_atual < len(self.frames_morte) - 1:
                    self.frame_atual += 1
                self.tempo_ultimo_frame = tempo_atual
            self.imagem_atual = self.frames_morte[self.frame_atual]
            return  # Impede a execução do restante da atualização

        # Resto da lógica de atualização para os outros estados (idle, run, attack, hit)
        if self.invencivel:
            if (tempo_atual - self.tempo_inicial_invencivel) >= TEMPO_INVENCIBILIDADE:
                self.invencivel = False

        if self.atacando:
            tempo_decorrido_corte = tempo_atual - self.tempo_ataque
            if tempo_decorrido_corte >= self.duracao_ataque:
                self.atacando = False
                self.set_estado('idle')
            else:
                self.frame_atual_corte = (tempo_decorrido_corte // self.tempo_por_frame) % len(self.frames_corte)
                self.rect_corte.center = (
                    self.rect_heroi.centerx + math.cos(self.angulo_corte) * 150,
                    self.rect_heroi.centery + math.sin(self.angulo_corte) * 150
                )

        if self.habilidade_especial_ativa:
            tempo_decorrido = tempo_atual - self.tempo_inicio_habilidade
            self.raio_habilidade = min(self.raio_maximo, tempo_decorrido * 0.5)
            if self.raio_habilidade >= self.raio_maximo:
                self.habilidade_especial_ativa = False
                self.raio_habilidade = 0

        if self.estado == 'hit':
            if (tempo_atual - self.tempo_hit) >= 1000:
                self.set_estado('idle')

        # Atualiza a animação (para estados que não são dead)
        if tempo_atual - self.tempo_ultimo_frame > self.tempo_por_frame:
            self.frame_atual += 1
            self.tempo_ultimo_frame = tempo_atual

        # Seleciona os frames com base no estado
        if self.estado == 'idle':
            frames = self.frames_idle
        elif self.estado == 'run':
            frames = self.frames_run
        elif self.estado == 'attack':
            frames = self.frames_attack
        elif self.estado == 'hit':
            frames = self.frames_dano
        else:
            frames = self.frames_idle

        self.frame_atual %= len(frames)
        self.imagem_atual = frames[self.frame_atual]

        # Inverte a imagem se o herói estiver virado para a esquerda
        if self.direcao == -1:
            self.imagem_atual = pygame.transform.flip(self.imagem_atual, True, False)


    def draw(self, tela):
        """
        Desenha o herói na tela, aplicando o efeito de dano se necessário.
        """
        if self.imagem_atual:
            # Cria uma cópia da imagem para aplicar a transparência e o efeito de dano
            imagem_com_efeito = self.imagem_atual.copy()

            # Aplica o efeito de dano (shader vermelho)
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_efeito_dano < TEMPO_EFEITO_DANO:
                # Cria uma surface vermelha e a aplica sobre a imagem
                vermelho = pygame.Surface(imagem_com_efeito.get_size(), pygame.SRCALPHA)
                vermelho.fill((255, 0, 0, 200))  # Vermelho com 80% de opacidade
                imagem_com_efeito.blit(vermelho, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

            # Desenha a imagem na tela
            tela.blit(imagem_com_efeito, self.rect_heroi)

        if self.habilidade_especial_ativa:
            superficie_transparente = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
            pygame.draw.circle(
                superficie_transparente,
                (255, 0, 0, 100),
                (self.rect_heroi.centerx, self.rect_heroi.centery),
                int(self.raio_habilidade))
            tela.blit(superficie_transparente, (0, 0))

    def desenhar_corte(self, tela):
        """Desenha o efeito de corte na tela, rotacionando-o com base no ângulo."""

        if self.estado == 'dead':
            return

        if self.atacando:
            # Obtém o frame atual do corte
            imagem_corte = self.frames_corte[self.frame_atual_corte]

            # Rotaciona a imagem do corte com base no ângulo (em radianos)
            angulo_graus = math.degrees(self.angulo_corte)  # Converte radianos para graus
            imagem_rotacionada = pygame.transform.rotate(imagem_corte, -angulo_graus)  # Rotaciona a imagem

            # Ajusta o retângulo da imagem rotacionada para manter o centro correto
            rect_rotacionado = imagem_rotacionada.get_rect(center=self.rect_corte.center)

            # Desenha a imagem rotacionada na tela
            tela.blit(imagem_rotacionada, rect_rotacionado)

    def receber_dano(self, dano):
        if self.estado == 'dead':
            return  # Não recebe dano se já estiver morto

        if not self.invencivel:
            self.vida_atual -= dano
            self.set_estado('hit')  # Muda para o estado de 'hit'
            self.tempo_hit = pygame.time.get_ticks()  # Inicia o temporizador de 'hit'
            self.tempo_efeito_dano = pygame.time.get_ticks()

            if self.vida_atual <= 0:
                self.vida_atual = 0
                self.set_estado('dead')  # Muda para o estado de morte
                self.tempo_morte = pygame.time.get_ticks()  # Inicia o temporizador de morte

            self.invencivel = True
            self.tempo_inicial_invencivel = pygame.time.get_ticks()

    def ativar_habilidade_especial(self):
        if self.habilidade_especial_disponivel and not self.habilidade_especial_ativa:
            self.habilidade_especial_ativa = True
            self.tempo_inicio_habilidade = pygame.time.get_ticks()
            self.habilidade_especial_disponivel = False
            self.contador_especial = 0
            self.efeito_fogo.iniciar()  # Inicia o efeito de fogo

    def ganhar_xp(self, quantidade):
        """
        Adiciona experiência ao herói e verifica se ele deve subir de nível.
        """
        self.xp += quantidade
        self.xp_atual += quantidade  # Adiciona a quantidade de XP ao XP atual

        # Verifica se o herói deve subir de nível
        if self.xp_atual >= self.xp_para_proximo_nivel:
            self.xp_atual -= self.xp_para_proximo_nivel  # Reduz o XP atual
            self.subir_nivel()  # Aumenta o nível e ajusta os atributos

    def subir_nivel(self):
        """
        Aumenta o nível do herói e ativa o estado de evolução.
        """
        self.nivel += 1
        self.xp_para_proximo_nivel = int(self.xp_para_proximo_nivel * 1.5)  # Aumenta a XP necessária para o próximo nível
        self.em_evolucao = True  # Ativa o estado de evolução
        print(f"Herói subiu para o nível {self.nivel}!")  # Debug: Mostra o novo nível

    def aumentar_vida(self):
        """Aumenta a vida máxima do herói."""
        self.vida_maxima += 20
        self.vida_atual = self.vida_maxima  # Restaura a vida ao máximo
        print(f"Vida máxima aumentada para {self.vida_maxima}")

    def aumentar_forca(self):
        """Aumenta o ataque do herói."""
        self.ataque += 10
        print(f"Ataque aumentado para {self.ataque}")

    def aumentar_velocidade(self):
        """Aumenta a velocidade do herói."""
        self.velocidade += 0.5
        print(f"Velocidade aumentada para {self.velocidade}")