import socket
from datetime import datetime
import time # Usaremos isso mais tarde no Cenário 3

# 1. Configurando o Servidor TCP (AF_INET = IPv4, SOCK_STREAM = TCP)
HOST = '127.0.0.1' # Endereço local (sua própria máquina)
PORT = 8080        # Porta onde o servidor vai "escutar"

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Evita erro de porta ocupada
servidor.bind((HOST, PORT))
servidor.listen(1) # O servidor começa a ouvir conexões

print(f"Servidor TCP do GuiaSense rodando em http://{HOST}:{PORT}")
print("Aguardando o navegador conectar...\n")

# 2. O Loop de Atendimento (Ele atende um por vez)
while True:
    # O accept() trava o código aqui até alguém abrir o navegador
    conexao, endereco_cliente = servidor.accept()
    
    # Lê o que o navegador pediu (A requisição HTTP GET)
    requisicao = conexao.recv(1024).decode('utf-8')
    if not requisicao:
        conexao.close()
        continue

    # 3. Descobrindo qual página o usuário quer acessar
    linha_pedido = requisicao.split('\n')[0]
    rota_pedida = linha_pedido.split(' ')[1]
    
    # 4. Registrando (Log) quem acessou e a hora
    hora_atual = datetime.now().strftime('%H:%M:%S')
    print(f"[{hora_atual}] IP {endereco_cliente[0]} pediu a página: {rota_pedida}")

    # --- CÓDIGO DO CENÁRIO 3 ---
    # time.sleep(3) 

    # 5. Criando a resposta que vai aparecer no navegador do usuário
    # Estilo CSS Unificado (Acessibilidade: Fontes grandes e alto contraste)
    estilo_acessivel = """
    <style>
        body { font-family: Arial, sans-serif; background-color: #ffffff; color: #000000; margin: 0; padding: 15px; font-size: 20px; }
        .container { max-width: 900px; margin: 0 auto; background: #ffffff; padding: 20px; border: 1px solid #333333; }
        h1 { color: #000000; font-size: 28px; text-align: center; margin-bottom: 15px; }
        .mapa { height: 400px; width: 100%; border: 1px solid #666666; margin: 15px 0; }
        .campo { margin-bottom: 20px; }
        label { display: block; font-weight: bold; margin-bottom: 5px; font-size: 20px; color: #333333; }
        input, select { width: 100%; padding: 10px; border: 1px solid #999999; font-size: 18px; background: #fafafa; box-sizing: border-box; }
        .btn-principal { background: #0055cc; color: white; width: 100%; padding: 15px; font-size: 20px; font-weight: bold; cursor: pointer; border: none; margin-top: 15px; }
        .btn-principal:hover { background: #0044aa; }
        .btn-voz { background: #cc0000; color: white; width: 100%; padding: 15px; font-size: 20px; font-weight: bold; cursor: pointer; border: none; margin-bottom: 20px; }
        .btn-voz:hover { background: #aa0000; }
        .status-header { background: #e6f2ff; padding: 15px; border: 1px solid #0055cc; margin-bottom: 20px; text-align: center; }
        .info-card { background: #f9f9f9; padding: 15px; border: 1px solid #cccccc; margin-top: 20px; }
        .gps-ponto { height: 16px; width: 16px; background-color: #cc0000; border-radius: 50%; display: inline-block; vertical-align: middle; }
    </style>
    """

    if rota_pedida == '/' or rota_pedida == '/config':
        cabecalho = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
        corpo = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <title>Portal GuiaSense - Configurar</title>
            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
            {estilo_acessivel}
        </head>
        <body>
            <div class="container">
                <h1>Portal GuiaSense</h1>
                
                <button class="btn-voz" onclick="alert('Assistente de Voz Ativado: Como posso ajudar?')">
                    ATIVAR AJUDA POR VOZ
                </button>

                <p style="text-align: center;">Busque o endereço ou clique no mapa.</p>
                
                <div id="map" class="mapa"></div>

                <form action="/status" method="GET">
                    <div class="campo">
                        <label>📍 Ponto de Partida:</label>
                        <div class="busca-container">
                            <input type="text" id="origem" name="origem" placeholder="Digite um local ou clique no mapa...">
                            <button type="button" class="btn-busca" onclick="buscarEndereco('origem')">🔍 Buscar</button>
                        </div>
                    </div>
                    
                    <div class="campo">
                        <label>Ponto de Chegada:</label>
                        <div class="busca-container">
                            <input type="text" id="destino" name="destino" placeholder="Digite um local ou clique no mapa...">
                            <button type="button" class="btn-busca" onclick="buscarEndereco('destino')">🔍 Buscar</button>
                        </div>
                    </div>

                    <div class="campo">
                        <label>Força da Vibração:</label>
                        <select name="vibracao">
                            <option value="Forte">Muito Forte (Recomendado)</option>
                            <option value="Media">Média</option>
                        </select>
                    </div>

                    <div class="campo">
                        <label>🔊 Volume do Som:</label>
                        <select name="som">
                            <option value="Alto">Som Alto</option>
                            <option value="Baixo">Som Baixo</option>
                        </select>
                    </div>

                    <button type="submit" class="btn-principal">SALVAR E COMEÇAR VIAGEM</button>
                </form>
            </div>

            <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
            <script>
                var map = L.map('map').setView([-1.455, -48.468], 14);
                L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png').addTo(map);
                
                var markerA, markerB, linha;

                // Função para atualizar marcadores e linha
                function atualizarMapa(lat, lng, tipo) {{
                    var latlng = [lat, lng];
                    if (tipo === 'origem') {{
                        if (markerA) map.removeLayer(markerA);
                        markerA = L.marker(latlng).addTo(map).bindPopup("Origem").openPopup();
                        document.getElementById('origem').value = lat.toFixed(5) + "," + lng.toFixed(5);
                    }} else {{
                        if (markerB) map.removeLayer(markerB);
                        markerB = L.marker(latlng).addTo(map).bindPopup("Destino").openPopup();
                        document.getElementById('destino').value = lat.toFixed(5) + "," + lng.toFixed(5);
                    }}
                    
                    if (markerA && markerB) {{
                        if (linha) map.removeLayer(linha);
                        linha = L.polyline([markerA.getLatLng(), markerB.getLatLng()], {{color: 'blue'}}).addTo(map);
                        map.fitBounds(linha.getBounds(), {{padding: [50, 50]}});
                    }} else {{
                        map.setView(latlng, 16);
                    }}
                }}

                // Clique no mapa
                map.on('click', function(e) {{
                    if (!markerA) {{
                        atualizarMapa(e.latlng.lat, e.latlng.lng, 'origem');
                    }} else if (!markerB) {{
                        atualizarMapa(e.latlng.lat, e.latlng.lng, 'destino');
                    }}
                }});

                // Busca por texto (Geocoding)
                async function buscarEndereco(idInput) {{
                    const query = document.getElementById(idInput).value;
                    if (query.length < 3) return alert("Digite um endereço mais específico.");
                    
                    try {{
                        const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${{encodeURIComponent(query)}}`);
                        const data = await response.json();
                        
                        if (data.length > 0) {{
                            const lat = parseFloat(data[0].lat);
                            const lon = parseFloat(data[0].lon);
                            atualizarMapa(lat, lon, idInput);
                        }} else {{
                            alert("Local não encontrado.");
                        }}
                    }} catch (erro) {{
                        alert("Erro ao buscar endereço.");
                    }}
                }}
            </script>
        </body>
        </html>
        """
        resposta = cabecalho + corpo

    elif rota_pedida.startswith('/status'):
        cabecalho = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
        corpo = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <title>Portal GuiaSense - Status</title>
            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
            {estilo_acessivel}
        </head>
        <body>
            <div class="container">
                <div class="status-header">
                    <h2 style="margin:0; color: #000000;">✔️ ROTA SINCRONIZADA</h2>
                </div>

                <button class="btn-voz" onclick="alert('Assistente de Voz Ativado: Como posso ajudar?')">
                     OUVIR INSTRUÇÕES (VOZ)
                </button>

                <div id="map" class="mapa"></div>

                <div class="info-card">
                    <p><strong><span class="gps-ponto"></span> Localização do GuiaSense:</strong> Em movimento...</p>
                    <p id="resumo-config"></p>
                </div>

                <button class="btn-principal" style="background: #666666;" onclick="window.location.href='/'">VOLTAR E ALTERAR</button>
            </div>

            <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
            <script>
                const params = new URLSearchParams(window.location.search);
                const o = params.get('origem')?.split(',');
                const d = params.get('destino')?.split(',');
                
                document.getElementById('resumo-config').innerHTML = "<b>Alerta:</b> Vibração " + params.get('vibracao') + " e " + params.get('som');
                
                const map = L.map('map').setView([o[0], o[1]], 15);
                L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png').addTo(map);

                L.marker([o[0], o[1]]).addTo(map).bindPopup("Início");
                L.marker([d[0], d[1]]).addTo(map).bindPopup("Fim");
                L.polyline([[o[0], o[1]], [d[0], d[1]]], {{color: 'blue', dashArray: '10'}}).addTo(map);
                
                // GPS (Ponto Vermelho) a caminho
                const latGps = parseFloat(o[0]) + (d[0] - o[0]) * 0.4;
                const lonGps = parseFloat(o[1]) + (d[1] - o[1]) * 0.4;
                L.circleMarker([latGps, lonGps], {{color: 'red', fillColor: '#f03', fillOpacity: 0.8, radius: 10}}).addTo(map).bindPopup("Você está aqui");
            </script>
        </body>
        </html>
        """
        resposta = cabecalho + corpo

    else: # 6. Tratamento de Erro 404
        cabecalho = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
        corpo = "<h1>Erro 404</h1><p>Página não encontrada.</p>"
        resposta = cabecalho + corpo

    # 7. Envia a resposta de volta para o Chrome/Edge e fecha a conexão
    conexao.sendall(resposta.encode('utf-8'))
    conexao.close()