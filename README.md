# Projeto GuiaSense: Comunicação TCP e UDP

Este projeto faz parte do ecossistema **GuiaSense**, simulando a integração entre uma interface de configuração via Web (TCP) e um sistema de alerta/voz de baixa latência (UDP).

## Estrutura do Projeto

O repositório contém três componentes principais:

1.  **`servidor_tcp.py`**: Atua como o Portal GuiaSense. É um servidor HTTP que entrega uma interface web para configuração de rotas e preferências de acessibilidade.
2.  **`servidor_udp.py`**: Simula a Central S.O.S, processando dados de voz. Possui uma lógica de descarte aleatório de 20% dos pacotes para simular instabilidades de rede realistas.
3.  **`cliente_udp.py`**: Ferramenta de diagnóstico que realiza testes de latência (RTT) e mede a perda de pacotes na comunicação de voz.



## Como Executar

### 1. Requisitos
* Python 3.x instalado.
* Não é necessário instalar bibliotecas externas (utiliza apenas `socket`, `time`, `random` e `datetime`).

### 2. Passo a Passo

#### **Cenário A: Portal de Configuração (TCP)**
1. No terminal, execute o servidor:
   ```bash
   python servidor_tcp.py

3. Abra o navegador e acesse: `http://127.0.0.1:8080`.
4. Interaja com o mapa e salve as configurações para ver o log de requisições no terminal.

#### **Cenário B: Teste de Latência de Voz (UDP)**
Para este teste, você precisará de dois terminais abertos:

***Terminal 1 (Servidor):***
  ```bash
  python servidor_udp.py
```

***Terminal 2 (Cliente):***
  ```bash
  python cliente_udp.py
```
