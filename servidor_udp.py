import socket
import random

HOST = '127.0.0.1'
PORT = 12000

# SOCK_DGRAM significa que é UDP
servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor.bind((HOST, PORT))

print(f"🎧 Central S.O.S GuiaSense escutando em {HOST}:{PORT}")

while True:
    mensagem, endereco_cliente = servidor.recvfrom(1024)
    
    # Simulando a internet da rua: 20% de chance de perder o pacote
    if random.randint(1, 10) <= 2:
        continue # Ignora o pacote de propósito para dar erro no cliente
        
    # Devolve a mensagem (o Eco)
    servidor.sendto(mensagem, endereco_cliente)
