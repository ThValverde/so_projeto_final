# Oficina do Noel

Um jogo educativo desenvolvido para a disciplina **SSC0640 - Sistemas Operacionais I**. O projeto simula conceitos de concorrência, sincronização e gerenciamento de recursos utilizando a biblioteca [Pygame](https://www.pygame.org/).

## Descrição

No jogo, você controla um ajudante do Papai Noel em uma oficina de presentes. Seu objetivo é coletar presentes das esteiras, processá-los na mesa e entregar o máximo possível, evitando perdas e gerenciando recursos limitados. O jogo utiliza analogias com problemas clássicos de sistemas operacionais, como o produtor-consumidor e uso de semáforos.

## Funcionalidades

- **Menu interativo** com opções de iniciar o jogo, ler o README e sair.
- **Tela de carregamento** sincronizada com áudio.
- **Mecânicas de jogo** baseadas em conceitos de SO (buffer, semáforos, escalonamento).
- **Pontuação** e condições de vitória/derrota.
- **Sprites animados** e interface gráfica amigável.

# 🎮 COMO JOGAR - Oficina do Noel

## 🎯 **OBJETIVO**
Gerencie a oficina do Papai Noel como um duende! Colete presentes das esteiras e organize-os na mesa de embrulho, vivenciando conceitos de Sistemas Operacionais de forma prática e divertida.

## 🕹️ **CONTROLES**
- **←/→ ou A/D**: Mover o duende entre as posições
- **ESPAÇO**: Coletar presente (em esteira) ou entregar na mesa
- **P**: Processar imediatamente (na mesa)
- **-**: Diminuir velocidade do processamento automático
- **ESC**: Voltar ao menu

## 📋 **COMO JOGAR**

### 1. **Posições do Duende**
O duende pode ocupar 4 posições:
- **Posições 1-3**: Abaixo das esteiras (para coletar presentes)
- **Posição 4**: Na mesa de embrulho (para entregar/processar presentes)

### 2. **Coletando Presentes**
- Mova o duende para baixo de uma esteira
- Aguarde um presente cair
- Pressione **ESPAÇO** quando o presente estiver próximo
- O duende ficará "carregando" o presente

### 3. **Entregando na Mesa**
- Com um presente em mãos, vá até a mesa (posição 4)
- Pressione **ESPAÇO** para entregar
- ⚠️ **Atenção**: A mesa comporta até 3 presentes!
- ⚠️ **Atenção**: O elfo carrega uma quantidade máxima de presentes, a depender do nível!

### 4. **Processando Presentes**
- Na mesa, pressione **Espaço** para descarregar o presente
- O processamento automático ocorre a cada 2 segundos
- Use **P** para processar imediatamente - na mesa
- Processar libera espaço na mesa e aumenta sua pontuação

### 5. **Vitória e Derrota**
- Atinja 300 pontos para vencer o jogo.
- Não deixe a desordem tomar conta. Você perde o jogo se sua penalidade se tornar muito alta: a regra é:
    Penalidade = Presentes Perdidos x 10
    - Você perde se: Penalidade >= Pontuação x 2

## 🧠 **CONCEITOS DE SO DEMONSTRADOS**

### **Threads**
- Cada esteira funciona em uma thread separada, produzindo presentes independentemente

### **Semáforos**
- A mesa é um recurso compartilhado com capacidade limitada, controlada por semáforo

### **Produtor-Consumidor**
- **Produtores**: Esteiras gerando presentes
- **Consumidor**: Duende coletando e processando
- **Buffer**: Mesa com espaço limitado

### **Escalonamento**
- A dificuldade aumenta automaticamente, simulando um escalonador de CPU

## 📊 **INTERFACE**
- **Pontuação**: Presentes processados
- **Nível**: Velocidade de produção
- **Mesa**: Ocupação atual (X/3)
- **Proc. Auto**: Status do processamento automático
- **Processados**: Total de presentes processados
- **Vel. Proc**: Tempo atual de processamento (segundos)
- **Perdidos**: Presentes não coletados
- **"Carregando Presente!"**: Duende está com presente
- **"Processando... X.Xs"**: Processamento em andamento

## ⚠️ **SITUAÇÕES ESPECIAIS**

### **Mesa Cheia**
- Não é possível entregar mais presentes
- **Demonstra**: Bloqueio por recurso limitado

### **Muitos Presentes Caindo**
- Priorize não deixar presentes caírem
- **Demonstra**: Pressão do escalonador

### **Sem Presentes na Mesa**
- Não é possível processar
- Colete e entregue presentes primeiro
- **Demonstra**: Buffer vazio no produtor-consumidor

## 🏆 **PONTUAÇÃO**
- **+10 pontos**: Cada presente processado
- **Objetivo**: Maximize a eficiência da oficina!
- **Desafio**: Quantos presentes você consegue processar?

---

**Divirta-se aprendendo Sistemas Operacionais na prática! 🎄🎁**

## Como Preparar e Executar o Jogo

1. Instale as dependências:
    ```bash
    pip install pygame
    ```
2. Execute o jogo:
    ```bash
    python main.py
    ```
3. Use as setas ou teclas `A/D` para mover, `Espaço` para interagir e `ESC` para voltar ao menu.

## Estrutura do Projeto

```
so_projeto_final/
├── game/
│   ├── main_game.py      # Lógica principal do jogo
│   └── mechanics.py      # Mecânicas e regras do jogo
├── ui/
│   ├── menu.py           # Tela de menu principal
│   └── screens.py        # Telas de carregamento e fim de jogo
├── main.py               # Ponto de entrada da aplicação
├── settings.py           # Configurações globais
├── assets/               # Imagens, áudios e fontes
└── README.md             # Este arquivo
```

## Créditos

- Desenvolvido por:
Felipe de Oliveira Gomes,
Leonardo Codeceira Gonçalves Pinto,
Leonardo Silva Cardoso e
Thiago de Castro Valverde
- Disciplina: SSC0640 - Sistemas Operacionais I
- Professor: Prof. Dr. Rodolfo I. Meneguette
- Universidade de São Paulo (USP)

## Licença

Este projeto é apenas para fins educacionais.