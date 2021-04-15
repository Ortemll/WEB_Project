from flask import *
from flask_login import login_user, login_required, LoginManager, logout_user, current_user

from orm import db_session

from orm.__all_models import *

from forms.LoginForm import LoginForm
from forms.RegisterForm import RegisterForm
from flask import make_response

# from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'pbkdf2:sha256:150000$DnBMMiBR$8d9d49127ae6e44c364f487f1233991db078d9ad32c' \
                           '789dc75e07ddd10ce7daa'


# api = Api(app)
# api.add_resource(users_resource.UsersResource, '/api/v2/users')
# api.add_resource(users_resource.UsersListResource, '/api/v2/users/<int:user_id>')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    db_sess = db_session.create_session()
    forums = db_sess.query(Forum).all()
    forums_and_discussions = {}
    for forum in forums:
        forums_and_discussions[forum] = db_sess.query(Discussion). \
            filter(Discussion.forum_id == forum.id)
    return render_template("index.html", slovar=forums_and_discussions)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        if len(form.password.data) < 5:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароль должен содержать 5 и более символов")

        if len(form.uniq_name.data) < 3:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Ник должен содержать 3 и более символов")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.uniq_name == form.uniq_name.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.uniq_name = form.uniq_name.data
        user.about = form.about.data
        user.vk_id = form.vk_id.data
        user.name = form.name.data if form.name.data else form.uniq_name.data
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()

        login_user(user, remember=form.remember_me.data)
        return redirect('/')
    return render_template('register.html', title='Reg', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        auth_index = form.user_auth_index.data
        if auth_index.startswith('@') and len(auth_index) == 1:
            render_template('login.html', title='Авторизация', form=form,
                            message='VK_id пуст')

        db_sess = db_session.create_session()
        if auth_index.startswith('@'):
            user = db_sess.query(User).filter(User.vk_id == auth_index[1:]).first()
        else:
            user = db_sess.query(User).filter(User.uniq_name == auth_index).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', title='Авторизация', form=form,
                               message='Пользователя с таким логином не существует')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/<int:id>', methods=['GET', 'POST'])
def discussion(id):
    db_sess = db_session.create_session()
    discussion = db_sess.query(Discussion).get(id)
    messages = db_sess.query(Message).filter(Message.discussion_id == discussion.id).all()
    return render_template("index_2.html", disc=discussion, mess=messages)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")



if __name__ == '__main__':
    db_session.global_init("orm/db/.db")
    # app.register_blueprint(jobs_api.blueprint)
    app.run(port=8080, host='127.0.0.1', debug=True)
