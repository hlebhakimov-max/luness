from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    songs = [
    {"name": "Нон стоп", "file": "music1.mp3"},
    {"name": "Адреналин", "file": "music2.mp3"},
    {"name": "Redbone", "file": "music3.mp3"},
    {"name": "Akkiemi", "file": "music4.mp3"}
    ]

    # ОШИБКА БЫЛА ТУТ: Обязательно должно быть слово 'return' в начале строки!
    return render_template('index.html', playlist=songs) 
    
    # Запуск сервера
if __name__ == '__main__':
    # debug=True позволяет видеть ошибки прямо в браузере
    app.run(debug=True)
    