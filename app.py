from flask import Flask, render_template

# Создаем приложение Flask
app = Flask(__name__)

@app.route('/')
def index():
    # Мы просто открываем главную страницу. 
    # Вся музыка теперь подгружается через JavaScript в браузере, 
    # чтобы обойти блокировки провайдера.
    return render_template('index.html')

if __name__ == '__main__':
    # Запуск сервера
    app.run(debug=True)
