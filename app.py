from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('query')
    if not query: return jsonify([])

    print(f"Джарвис: масштабный поиск (50 результатов) для: {query}")

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'default_search': 'ytsearch50', # Лимит увеличен до 50
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch50:{query} audio", download=False)
            results = []
            if 'entries' in info:
                for entry in info['entries']:
                    if entry:
                        results.append({
                            'id': entry.get('id'),
                            'title': entry.get('title'),
                            'artist': entry.get('uploader'),
                            'url': entry.get('url'),
                            'cover': entry.get('thumbnail')
                        })
            return jsonify(results)
    except Exception as e:
        print(f"Ошибка: {e}")
        return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)
