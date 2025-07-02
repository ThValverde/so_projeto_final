# 🎮 COMO JOGAR - Oficina do Noel

## 🎯 **OBJETIVO**
Ajude o duende a gerenciar a oficina do Papai Noel! Colete presentes das esteiras e organize-os na mesa de embrulho, demonstrando conceitos de Sistemas Operacionais na prática.

## 🕹️ **CONTROLES**
- **←/→ ou A/D**: Mover o duende entre as posições
- **ESPAÇO**: Coletar presente (estando em esteira) OU entregar na mesa
- **C**: Processar presente da mesa (simula consumo manual)
- **P**: Forçar processamento da mesa (quando estiver na posição da mesa)
- **T**: Alternar processamento automático (Liga/Desliga)
- **+/=**: Acelerar processamento automático da mesa
- **-**: Desacelerar processamento automático da mesa
- **ESC**: Voltar ao menu

## 📋 **COMO JOGAR**

### 1. **Posições do Duende**
O duende pode ficar em 4 posições:
- **Posições 1-3**: Embaixo das esteiras (para coletar presentes)
- **Posição 4**: Na mesa de embrulho (para entregar/processar)

### 2. **Coletando Presentes**
- Mova o duende para ficar embaixo de uma esteira
- Aguarde um presente cair
- Pressione **ESPAÇO** quando o presente estiver próximo
- O duende ficará "carregando" o presente

### 3. **Entregando na Mesa**
- Com um presente em mãos, vá até a mesa (posição 4)
- Pressione **ESPAÇO** para entregar
- ⚠️ **ATENÇÃO**: A mesa tem capacidade limitada (3 presentes)!

### 4. **Processando Presentes**
- Na mesa, pressione **C** para processar um presente manualmente
- A mesa também **processa automaticamente** a cada 3 segundos
- Pressione **T** para ligar/desligar o processamento automático
- Use **+/-** para ajustar a velocidade de processamento
- Pressione **P** para forçar um processamento imediato
- Processamento libera espaço na mesa e aumenta pontuação

## 🧠 **CONCEITOS DE SO DEMONSTRADOS**

### **Threads (Fios de Execução)**
- Cada esteira roda em uma thread separada
- Produzem presentes independentemente do jogo

### **Semáforos**
- A mesa tem capacidade limitada (recurso compartilhado)
- Semáforo controla quantos presentes podem ficar na mesa
- Se mesa cheia = bloqueio até processar

### **Produtor-Consumidor**
- **Produtores**: Esteiras gerando presentes
- **Consumidor**: Duende coletando e processando
- **Buffer**: Mesa com capacidade limitada

### **Escalonamento**
- Dificuldade aumenta automaticamente (mais presentes)
- Simula escalonador de CPU aumentando prioridades

## 📊 **INTERFACE**
- **Pontuação**: Presentes processados com sucesso
- **Nível**: Velocidade atual de produção
- **Mesa**: Ocupação da mesa (X/3)
- **Proc. Auto**: Status do processamento automático (ATIVO/PAUSADO)
- **Processados**: Total de presentes processados pela mesa
- **Vel. Proc**: Velocidade atual de processamento em segundos
- **Perdidos**: Presentes que caíram sem ser coletados
- **"Carregando Presente!"**: Indica que duende tem presente
- **"Processando... X.Xs"**: Indica processamento em andamento na mesa

## 🎯 **ESTRATÉGIAS**

### **Iniciante**
1. Foque em uma esteira por vez
2. Colete presente → Entregue na mesa → Processe
3. Não deixe a mesa encher

### **Avançado**
1. Use processamento automático para eficiência
2. Ajuste velocidade de processamento conforme necessário
3. Monitore várias esteiras simultaneamente
4. Balance coleta vs. entrega vs. velocidade de processamento
5. Use processamento manual (P) para emergências

### **Expert**
1. Preveja quando esteiras vão produzir
2. Posicione-se estrategicamente
3. Otimize velocidade de processamento para máximo throughput
4. Use processamento manual apenas quando necessário
5. Balance automático vs. manual conforme situação

## ⚠️ **SITUAÇÕES ESPECIAIS**

### **Mesa Cheia**
- Não consegue entregar mais presentes
- Precisa processar (tecla C) para liberar espaço
- **Demonstra**: Bloqueio por recurso limitado

### **Muitos Presentes Caindo**
- Priorize não deixar cair
- **Demonstra**: Pressão do escalonador

### **Sem Presentes na Mesa**
- Não consegue processar
- Precisa coletar e entregar primeiro
- **Demonstra**: Buffer vazio no produtor-consumidor

## 🏆 **PONTUAÇÃO**
- **+10 pontos**: Cada presente processado
- **Objetivo**: Maximize a eficiência da oficina!
- **Desafio**: Quantos presentes você consegue processar?

---
**Divirta-se aprendendo Sistemas Operacionais na prática! 🎄🎁**
