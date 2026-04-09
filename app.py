import requests
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    query = request.args.get('search', 'Top Hits')
    # Используем HTTP вместо HTTPS для теста (иногда помогает обойти блокировки)
    url = "http://apple.com"
    params = {'term': query, 'media': 'music', 'limit': 20}
    
    tracks = []
    error_msg = None # Сюда запишем реальную ошибку

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        for item in data.get('results', []):
            tracks.append({
                'title': item.get('trackName'),
                'artist': {'name': item.get('artistName')},
                'album': {'cover_medium': item.get('artworkUrl100')},
                'preview': item.get('previewUrl')
            })
            
        if not tracks:
            error_msg = f"Ничего не найдено по запросу '{query}'"

    except Exception as e:
        # Теперь мы увидим РЕАЛЬНУЮ причину на сайте
        error_msg = f"Техническая ошибка: {str(e)}"

    # Если есть ошибка, создаем одну карточку с текстом ошибки
    if error_msg and not tracks:
        tracks = [{
            'title': "Внимание",
            'artist': {'name': error_msg},
            'album': {'cover_medium': "https://placeholder.com"},
            'preview': ""
        }]

    return render_template('index.html', tracks=tracks, query=query)

if __name__ == '__main__':
    app.run(debug=True)
