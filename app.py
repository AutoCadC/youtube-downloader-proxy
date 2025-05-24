import os
from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import requests

app = Flask(__name__ )
CORS(app)  # Habilita CORS para todas as rotas

# Configurações da API do RapidAPI
RAPIDAPI_HOST = "youtube-video-fast-downloader-24-7.p.rapidapi.com"
RAPIDAPI_KEY = "96723e62ecmsha9589677a0185efp1344a2jsn5364072d5d07"

@app.route('/')
def index():
    return jsonify({
        "status": "online",
        "message": "YouTube Downloader API Proxy está funcionando!"
    })

@app.route('/api/download/audio/<video_id>')
def download_audio(video_id):
    """Proxy para download de áudio"""
    try:
        quality = request.args.get('quality', '251')  # Qualidade padrão: alta (160 kbps)
        
        url = f"https://{RAPIDAPI_HOST}/download_audio/{video_id}?quality={quality}"
        
        headers = {
            "x-rapidapi-host": RAPIDAPI_HOST,
            "x-rapidapi-key": RAPIDAPI_KEY
        }
        
        # Fazer a requisição para a API do RapidAPI
        response = requests.get(url, headers=headers, stream=True )
        
        # Se a resposta for um redirecionamento, retornar a URL de redirecionamento
        if response.status_code in (301, 302, 303, 307, 308):
            return jsonify({"redirect_url": response.headers['Location']})
        
        # Se for um erro, retornar a mensagem de erro
        if response.status_code != 200:
            return jsonify(response.json()), response.status_code
        
        # Se for um download direto, transmitir o conteúdo
        def generate():
            for chunk in response.iter_content(chunk_size=4096):
                yield chunk
        
        # Obter os headers da resposta original
        headers = {}
        for name, value in response.headers.items():
            if name.lower() not in ('transfer-encoding', 'connection'):
                headers[name] = value
        
        return Response(
            stream_with_context(generate()),
            headers=headers,
            content_type=response.headers.get('content-type', 'application/octet-stream')
        )
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/download/video/<video_id>')
def download_video(video_id):
    """Proxy para download de vídeo"""
    try:
        quality = request.args.get('quality', '22')  # Qualidade padrão: 720p
        
        url = f"https://{RAPIDAPI_HOST}/download_video/{video_id}?quality={quality}"
        
        headers = {
            "x-rapidapi-host": RAPIDAPI_HOST,
            "x-rapidapi-key": RAPIDAPI_KEY
        }
        
        # Fazer a requisição para a API do RapidAPI
        response = requests.get(url, headers=headers, stream=True )
        
        # Se a resposta for um redirecionamento, retornar a URL de redirecionamento
        if response.status_code in (301, 302, 303, 307, 308):
            return jsonify({"redirect_url": response.headers['Location']})
        
        # Se for um erro, retornar a mensagem de erro
        if response.status_code != 200:
            return jsonify(response.json()), response.status_code
        
        # Se for um download direto, transmitir o conteúdo
        def generate():
            for chunk in response.iter_content(chunk_size=4096):
                yield chunk
        
        # Obter os headers da resposta original
        headers = {}
        for name, value in response.headers.items():
            if name.lower() not in ('transfer-encoding', 'connection'):
                headers[name] = value
        
        return Response(
            stream_with_context(generate()),
            headers=headers,
            content_type=response.headers.get('content-type', 'application/octet-stream')
        )
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Usar 0.0.0.0 para permitir acesso externo
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
