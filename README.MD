# Hack'n'Slash - Secret wave

Este é um protótipo de jogo em Python no estilo Hack'n'Slash, onde o 
herói permanece no centro da tela, enquanto hordas de monstros o perseguem.


# Estrutura do Projeto
======================

 
HacknSlash-SecretWave/                          
│
├── assets/             
│   └── Drop/   
│           └── Vida/
│                     └── Vida_1.png
│                     └── Vida_2.png
│                     └── Vida_3.png
│                     └── Vida_4.png
│                     └── Vida_5.png
│                     └── Vida_6.png
│                     └── Vida_7.png
│                     └── Vida_8.png
│           └── XP/
│                     └── XP_1.png
│                     └── XP_2.png
│                     └── XP_3.png
│                     └── XP_4.png
│                     └── XP_5.png
│                     └── XP_6.png
│                     └── XP_7.png
│                     └── XP_8.png
│                     └── XP_9.png
│                     └── XP_10.png             
│   └── Efeito_espada/   
│           └── Corte_1.png
│           └── Corte_2.png
│           └── Corte_3.png
│           └── Corte_4.png
│           └── Corte_5.png
│           └── Corte_6.png        
│   └── Fogo/   
│           └── Fogo_1.png
│           └── Fogo_2.png
│           └── Fogo_3.png
│           └── Fogo_4.png
│           └── Fogo_5.png
│           └── Fogo_6.png   
│           └── Fogo_7.png
│           └── Fogo_8.png
│           └── Fogo_9.png
│           └── Fogo_10.png
│           └── Fogo_11.png
│           └── Fogo_12.png   
│   └── fonts/  
|            └── Bitwise.ttf
│   └── Heroi/
│           └── 01-Parado/
│                     └── Parado_1.png
│                     └── Parado_2.png
│                     └── Parado_3.png
│                     └── Parado_4.png
│                     └── Parado_5.png
│                     └── Parado_6.png
│                     └── Parado_7.png
│                     └── Parado_8.png
│                     └── Parado_9.png
│                     └── Parado_10.png
│                     └── Parado_11.png
│                     └── Parado_12.png
│           └── 02-Corrida/
│                     └── Corrida_1.png
│                     └── Corrida_2.png
│                     └── Corrida_3.png
│                     └── Corrida_4.png
│                     └── Corrida_5.png
│                     └── Corrida_6.png
│                     └── Corrida_7.png
│                     └── Corrida_8.png
│                     └── Corrida_9.png
│                     └── Corrida_10.png
│           └── 03-Ataque/
│                     └── No_Effect/
│                     			└── Ataque_1.png
│                     			└── Ataque_2.png
│                     			└── Ataque_3.png
│                     			└── Ataque_4.png
│                     			└── Ataque_5.png
│                     			└── Ataque_6.png
│                     			└── Ataque_7.png
│                     			└── Ataque_8.png
│           └── 04-Dano/
│                     └── Dano_1.png
│                     └── Dano_2.png
│                     └── Dano_3.png
│                     └── Dano_4.png
│                     └── Dano_5.png
│                     └── Dano_6.png
│           └── 05-Morte/
│                     └── Morte_1.png
│                     └── Morte_2.png
│                     └── Morte_3.png
│                     └── Morte_4.png
│                     └── Morte_5.png
│                     └── Morte_6.png
│                     └── Morte_7.png
│                     └── Morte_8.png
│   └── Menu/
│           └── Menu_1.png
│           └── Menu_2.png
│           └── Menu_3.png
│           └── Menu_4.png
│           └── Menu_5.png
│           └── trofeu_1.png
│   └── Monstro/
│           └── Monstro_Andando/
│                     └── Andando_1.png
│                     └── Andando_2.png
│           └── Monstro_Hit/
│                     └── hit_6.png
│   └── Mouse/
│           └── Click/
│                     └── Click_1.png
│           └── Idle/
│                     └── Indle_1.png
│   └── Sons/
│           └── ataque.mp3
│           └── fire_ataque.mp3
│           └── game_over.mp3
│           └── level_up.mp3
│           └── musica_fundo.mp3
│           └── start.mp3
│   └── fundo_tile.png  
│   └── icon.png     
│   └── icon.ico                
│
│
├── configuracoes.py                          
├── funcoes.py                       
├── hud.py                          
├── jogador.py                       
├── main.ico                    
├── monstro.spec                  
├── README.md                      
└── waves.py   
└── leaderboard.json                          


## Executando

Basta rodar:
   python main.py

## Lógica de jogo

- O herói começa com 100 de vida.
- A cada golpe com o clique do mouse, realiza um ataque que causa dano nos inimigos.
- Com uma pontuacao de 50, o heroi pode realizar um ataque especial 
- Os monstros surgem em ondas (waves), cada uma durando 15 segundos e 5 segundos de descanso.
- Cada monstro derrotado concede XP ao herói, que sobe de nível, inicialmente 100 XP e depois aumentando conforme vai ganhando niveis.
- Ao subir de nivel, o heroi pode escolher entre aumentar sua vida, força ou sua velocidade
- Ao final do jogo, os registros de pontuação e nome serão armazenados em um arquivo json para ver exibido no placar
