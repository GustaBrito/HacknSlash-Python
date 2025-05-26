# 🎮 Hack'n'Slash - Secret Wave

Um jogo 2D de ação desenvolvido em **Python** com **Pygame**, onde o jogador controla um herói em um mundo repleto de monstros.  
O jogo inclui sistema de **combate**, **evolução de personagem**, **waves progressivas** e um **leaderboard competitivo**.

---

## 📸 Screenshots do Jogo

### 🧑‍💻 1. HUD do Jogador  
<img src="IMG_9021.png" alt="Status do Jogador" width="500"/>  

Exibe informações vitais do personagem:
- ❤️ Vida: 12/103
- 💪 Força: 8
- 🏃 Velocidade: 35

Também mostra o nível atual e o progresso da wave.

---

### 🔧 2. Menu de Evolução  
<img src="IMG_9025.png" alt="Menu de Upgrade" width="500"/>  

Quando o jogador acumula **XP suficiente**, pode escolher entre:
1. ➕ +20 Vida
2. ➕ +2 Força
3. ➕ +0.5 Velocidade

---

### ☠️ 3. Tela de Game Over  
<img src="IMG_9026.png" alt="Game Over" width="500"/>  

Ao morrer, o jogador vê:
- Estatísticas da partida (tempo, wave alcançada, nível máximo)
- Opção para digitar seu nome e salvar no leaderboard
- Botões para voltar ao menu ou sair do jogo

---

### 🏆 4. Leaderboard  
<img src="IMG_9027.png" alt="Placar de Líderes" width="500"/>  

Ranking dos melhores jogadores com:
- Nome
- Pontuação
- Data do recorde
- Botão para voltar ao menu

---

## 🛠️ Funcionalidades Principais

- ⚔️ **Sistema de Combate**: Ataques básicos e habilidade especial.
- 📈 **Progressão**: Evolução de atributos (vida, força, velocidade).
- 🌊 **Waves**: Inimigos com dificuldade progressiva.
- 💾 **Persistência**: Leaderboard salvo em arquivo `.json`.
- 🖥️ **Build Executável**: Versão compilada para Windows (`.exe`).

---

## 📥 Como Jogar

### 🎮 Controles
- **WASD**: Movimento
- **Clique do Mouse**: Ataque básico
- **Espaço**: Habilidade especial

### 🚀 Execução
```bash
python main.py
```

---

📌 Destaques Técnicos
🗂️ Arquitetura modular (separação em jogador.py, monstro.py, waves.py).

💾 Sistema de save/load para o leaderboard.

✨ Efeitos visuais de dano e animações fluidas.

🛠️ Build automatizada com PyInstaller.

<div align="center">
```
HacknSlash-SecretWave/
│
├── assets/
│   ├── Drop/
│   │   ├── Vida/
│   │   └── XP/
│   ├── Efeito_espada/
│   ├── Fogo/
│   ├── fonts/
│   ├── Heroi/
│   │   ├── 01-Parado/
│   │   ├── 02-Corrida/
│   │   ├── 03-Ataque/No_Effect/
│   │   ├── 04-Dano/
│   │   └── 05-Morte/
│   ├── Menu/
│   ├── Monstro/
│   │   ├── Monstro_Andando/
│   │   └── Monstro_Hit/
│   ├── Mouse/
│   │   ├── Click/
│   │   └── Idle/
│   ├── Sons/
│   ├── fundo_tile.png
│   ├── icon.png
│   └── icon.ico
│
├── configuracoes.py
├── funcoes.py
├── hud.py
├── jogador.py
├── main.ico
├── monstro.spec
├── README.md
├── waves.py
└── leaderboard.json
```
</div>

🧠 Lógica de Jogo
🛡️ O herói começa com 100 de vida.

🖱️ Cada golpe com o clique do mouse realiza um ataque que causa dano aos inimigos.

⭐ Ao atingir 50 pontos, o herói pode realizar um ataque especial.

🌊 Os monstros surgem em ondas (waves), cada uma com:

15 segundos de combate

5 segundos de descanso

🏆 Cada monstro derrotado concede XP ao herói, que sobe de nível:

Inicialmente precisa de 100 XP

Depois, a necessidade aumenta conforme evolui.

➕ Ao subir de nível, o herói pode escolher entre:

Aumentar a vida

Aumentar a força

Aumentar a velocidade

💾 Ao final do jogo, as pontuações e nomes são armazenados em um arquivo .json para exibição no placar.





