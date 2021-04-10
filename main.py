from flask import *
from flask_login import login_user, login_required, LoginManager, logout_user, current_user

from orm import db_session

from orm.Forums_db import Forums
from orm.Discussions_db import Discussions
from orm.Messages_db import Messages
from orm.User_db import User

from forms.LoginForm import LoginForm
from forms.user import RegisterForm
from sqlalchemy_serializer import *
from flask import make_response
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'pbkdf2:sha256:150000$DnBMMiBR$8d9d49127ae6e44c364f487f1233991db078d9ad32c' \
                           '789dc75e07ddd10ce7daa'


# api.add_resource(users_resource.UsersResource, '/api/v2/users')

# api.add_resource(users_resource.UsersListResource, '/api/v2/users/<int:user_id>')

def main():
    db_session.global_init("orm/db/test_2.db")
    # app.register_blueprint(jobs_api.blueprint)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def main_2():
    db_sess = db_session.create_session()
    db_sess.commit()
    return render_template("index.html")


@app.route('/a')
def discution():
    return render_template("index_2.html")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.networks == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            networks=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Reg', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    message = ''
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.networks == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        else:
            message = 'Wrong'
            db_sess.commit()
    return render_template('login.html', title='Авторизация', form=form, message=message)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    main()
    app.run(port=8080, host='127.0.0.1', debug=True)
