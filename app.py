import requests
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    query = request.args.get('search', 'Top Hits')
    url = "https://apple.com"
    params = {'term': query, 'media': 'music', 'limit': 20}
    
    tracks = []
    try:
        response = requests.get(url, params=params, timeout=10)
        # Если ответ не JSON, это вызовет ошибку, которую мы поймаем ниже
        data = response.json()
        
        for item in data.get('results', []):
            tracks.append({
                'title': item.get('trackName'),
                'artist': {'name': item.get('artistName')},
                'album': {'cover_medium': item.get('artworkUrl100')},
                'preview': item.get('previewUrl')
            })
    except Exception as e:
        print(f"--- Ошибка сети: {e} ---")
        # ТЕСТОВАЯ ПЕСНЯ (если интернет не работает)
        tracks = [{
            'title': "Ошибка подключения к API",
            'artist': {'name': "Проверьте интернет или VPN"},
            'album': {'cover_medium': "https://placeholder.com"},
            'preview': ""
        }]

    return render_template('index.html', tracks=tracks, query=query)

if __name__ == '__main__':
    app.run(debug=True)
