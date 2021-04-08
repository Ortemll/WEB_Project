from flask import Flask, url_for, render_template, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/', methods=['GET'])
def index():
    # Реализовать с нормальным пользователем!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    return render_template('main_form.html', title='Главная страница', user_is_registered=False)


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html', title='Регистрация')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
