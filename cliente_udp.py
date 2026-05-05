import socket
import time

HOST = '127.0.0.1'
PORT = 12000

cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# REGRA DE OURO: Se demorar mais de 1 segundo, considere perdido (Timeout)
cliente.settimeout(1.0) 

rtts = []
perdidos = 0
total = 10

print("Iniciando Teste de Latência da Voz (S.O.S UDP)...\n")

for i in range(1, total + 1):
    msg = f"Ping {i} - Teste de Voz".encode('utf-8')
    
    # Marca a hora de saída
    tempo_saida = time.time()
    
    try:
        cliente.sendto(msg, (HOST, PORT))
        resposta, endereco = cliente.recvfrom(1024)
        
        # Marca a hora de chegada
        tempo_chegada = time.time()
        
        # Calcula o RTT em milissegundos
        rtt = (tempo_chegada - tempo_saida) * 1000
        rtts.append(rtt)
        print(f"Recebido de {endereco[0]}: seq={i} tempo={rtt:.2f} ms")
        
    except socket.timeout:
        # Caiu aqui? O pacote se perdeu e deu timeout.
        perdidos += 1
        print(f"❌ Falha: Pacote {i} perdido (Timeout de 1s estourou)")

# Estatísticas finais pedidas pelo professor
print("\n--- Estatísticas Finais ---")
print(f"Enviados: {total} | Recebidos: {len(rtts)} | Perdidos: {perdidos} ({(perdidos/total)*100}% de perda)")
if rtts:
    print(f"RTT Médio da Chamada: {(sum(rtts)/len(rtts)):.2f} ms")

cliente.close()
