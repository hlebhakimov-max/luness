import requests
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    query = request.args.get('search', 'Top Hits')
    
    # ПЛАН "ХАКЕР": Используем другой домен, который сложнее подменить
    # И добавляем проверку, чтобы requests не ходил на www
    url = "https://jamendo.com"
    params = {
        'client_id': '56d30cce',
        'format': 'json',
        'limit': 20,
        'search': query
    }
    
    tracks = []
    try:
        # allow_redirects=False запретит системе перекидывать нас на www.jamendo.com
        response = requests.get(url, params=params, timeout=10, allow_redirects=False)
        
        print(f"--- АДРЕС: {response.url} ---")
        
        if response.status_code == 200:
            data = response.json()
            for item in data.get('results', []):
                tracks.append({
                    'title': item.get('name'),
                    'artist': {'name': item.get('artist_name')},
                    'album': {'cover_medium': item.get('image')},
                    'preview': item.get('audio')
                })
        else:
            print(f"--- СТАТУС: {response.status_code}. Возможно, редирект на www ---")
            
    except Exception as e:
        print(f"--- ОШИБКА: {e} ---")

    if not tracks:
        tracks = [{'title': 'Блокировка API', 'artist': {'name': 'Ваш провайдер подменяет адрес'}, 'album': {'cover_medium': ''}, 'preview': ''}]

    return render_template('index.html', tracks=tracks, query=query)

if __name__ == '__main__':
    app.run(debug=True)
