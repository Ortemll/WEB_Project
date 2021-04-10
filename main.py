from flask import Flask, url_for, render_template, request
from orm import db_session
from orm.__all_models import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pbkdf2:sha256:150000$DnBMMiBR$8d9d49127ae6e44c364f487f1233991db078d9ad32c789dc75e07ddd10ce7daa'


@app.route('/', methods=['GET'])
def index():
    # Реализовать с нормальным пользователем!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    return render_template('main_form.html', title='Главная страница', user_is_registered=False)


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html', title='Регистрация')


def main():
    db_session.global_init("orm/db/.db")

    # app.run(port=8080, host='127.0.0.1', debug=True)


if __name__ == '__main__':
    main()