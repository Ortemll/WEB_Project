from flask import *
from flask_login import login_user, login_required, LoginManager, logout_user, current_user
import os
from orm import db_session
import requests
from orm.__all_models import *

from forms.LoginForm import LoginForm
from forms.RegisterForm import RegisterForm
from forms.PhotoLoaderForm import PhotoLoader
from flask_wtf.csrf import CSRFProtect
from flask import make_response
import pandas as pd
import cx_Oracle
import PIL
from flask import request
from werkzeug.datastructures import CombinedMultiDict
from PIL import Image
import base64
import io
import cv2

# from flask_restful import reqparse, abort, Api, Resource

csrf = CSRFProtect()

app = Flask(__name__, template_folder="./templates/")
login_manager = LoginManager()
login_manager.init_app(app)
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024
app.config['SECRET_KEY'] = 'pbkdf2:sha256:150000$DnBMMiBR$8d9d49127ae6e44c364f487f1233991db078d9ad32c' \
                           '789dc75e07ddd10ce7daa'
csrf.init_app(app)

# api = Api(app)
# api.add_resource(users_resource.UsersResource, '/api/v2/users')
# api.add_resource(users_resource.UsersListResource, '/api/v2/users/<int:user_id>')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
def index():
    forum_form = ForumForm()
    discussion_form = DiscussionForm()
    db_sess = db_session.create_session()

    if request.method == 'POST':
        if request.form.get('delete_discussion'):
            disc_to_delete = db_sess.query(Discussion).get(request.form['delete_discussion'])
            for message in disc_to_delete.messages:
                db_sess.delete(message)
            db_sess.delete(disc_to_delete)
            db_sess.commit()
        elif request.form.get('delete_forum'):
            forum_to_delete = db_sess.query(Forum).get(request.form['delete_forum'])
            for disc_to_delete in forum_to_delete.discussions:
                for message in disc_to_delete.messages:
                    db_sess.delete(message)
                db_sess.delete(disc_to_delete)
            db_sess.delete(forum_to_delete)
            db_sess.commit()

    if forum_form.forum_submit.data and forum_form.validate():
        forum = Forum(title=forum_form.forum_title.data, creator_id=current_user.id)
        db_sess.add(forum)
        db_sess.commit()
        forum_form.forum_title.data = None

    if discussion_form.discussion_submit.data and discussion_form.validate():
        discussion = Discussion(title=discussion_form.discussion_title.data, forum_id=request.form['forum_id'],
                                creator_id=current_user.id)
        db_sess.add(discussion)
        db_sess.commit()
        message = Message(user_id=current_user.id, content=discussion_form.message.data, discussion_id=discussion.id)
        db_sess.add(message)
        db_sess.commit()

        discussion_form.discussion_title.data = None
        discussion_form.message.data = None
        return redirect(f'/discussion/{discussion.id}')

    forums = db_sess.query(Forum).all()
    forums_and_discussions = {forum: forum.discussions for forum in forums}

    return render_template("index.html", slovar=forums_and_discussions,
                           discussion_form=discussion_form, forum_form=forum_form)


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
        if form.vk_id.data:
            if db_sess.query(User).filter(User.vk_id == form.vk_id.data).first():
                return render_template('register.html', title='Регистрация', form=form,
                                       message="Такой vk_id уже есть")
            vk_id_int = requests.get(f'https://vk.com/{form.vk_id.data}')
            vk_id_str = requests.get(f'https://vk.com/id{form.vk_id.data}')
            if not vk_id_int and not vk_id_str:
                return render_template('register.html', title='Регистрация', form=form,
                                       message="Такой vk_id не существует")

        user = User()
        user.uniq_name = form.uniq_name.data
        user.about = form.about.data
        user.vk_id = form.vk_id.data
        user.name = form.name.data if form.name.data else form.uniq_name.data
        user.set_password(form.password.data)
        user.profile_picture = user.conver_to_binary(r'C:\Users\Moxim\PycharmProjects\web_new\WEB_Project-main\static\img\default_image.jpg')
        db_sess.add(user)
        db_sess.commit()

        login_user(user, remember=form.remember_me.data)
        #img_to_save = Image.open(io.BytesIO(current_user.profile_picture))
        #img_to_save.save(rf'C:\Users\Moxim\PycharmProjects\web_new\WEB_Project\static\img\{current_user.id}.jpg', "PNG")
        return redirect('/register/load_photo')
    return render_template('register.html', title='Reg', form=form)


@app.route('/register/load_photo', methods=['GET', 'POST'])
def load():
    form = PhotoLoader()
    if form.submit.data:
        if form.image.data is not None:
            db_sess = db_session.create_session()
            f = form.image.data
            filename = secure_filename(f.filename)
            f.save(rf'C:\Users\Moxim\PycharmProjects\web_new\WEB_Project\static\img\{filename}')
            current_user.profile_picture_name = filename
            current_user.profile_picture = current_user.conver_to_binary(rf'C:\Users\Moxim\PycharmProjects\web_new\WEB_Project\static\img\{filename}')
            db_sess.merge(current_user)
            db_sess.commit()
            return render_template('LoadPhoto.html', title='Load Photo', form=form)
    return render_template('LoadPhoto.html', title='Load Photo', form=form)


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


@app.route('/user/<int:id>')
def info_about_user(id):
    return render_template("Home_page.html", title='Домашняя страница')


@app.route('/discussion/<int:id>', methods=['GET', 'POST'])
def discussion(id):
    db_sess = db_session.create_session()
    discussion = db_sess.query(Discussion).get(id)
    message_form = MessageForm()
    # реализовать лайки и дизлайкиииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииии
    if request.method == 'POST':
        if request.form.get('delete_comment'):
            for comment in db_sess.query(Message).filter(
                    Message.answers_to_id == request.form['delete_comment']).all():
                comment.answers_to_id = None
                db_sess.merge(comment)
            db_sess.delete(db_sess.query(Message).get(request.form['delete_comment']))
            db_sess.commit()
        # elif request.form.get('like'):
        #     liked_mess = db_sess.query(Message).get(request.form['like'])
        #     liked_mess.likes += 1
        #     db_sess.merge(liked_mess)
        #     db_sess.commit()
        # elif  request.form.get('dislike'):
        #     disliked_mess = db_sess.query(Message).get(request.form['dislike'])
        #     disliked_mess.likes += 1
        #     db_sess.merge(disliked_mess)
        #     db_sess.commit()

    if message_form.validate_on_submit():
        message = Message(user_id=current_user.id, content=message_form.message.data,
                          discussion_id=discussion.id)
        if request.form.get('answers_to_id'):
            message.answers_to_id = request.form['answers_to_id']
        db_sess.add(message)
        db_sess.commit()
        message_form.message.data = None

    messages_and_answers = {mes: [] for mes in filter(lambda el: el.answers_to_id is None,
                                                      discussion.messages)}

    for el in filter(lambda el: el.answers_to_id is not None, discussion.messages):
        curr_message = el
        answered_by_curr = db_sess.query(Message).get(curr_message.answers_to_id)
        while answered_by_curr not in messages_and_answers.keys():
            curr_message = answered_by_curr
            answered_by_curr = db_sess.query(Message).get(curr_message.answers_to_id)
        messages_and_answers[answered_by_curr].append(el)

    return render_template("discussion.html", discussion=discussion,
                           messages_and_answers=messages_and_answers,
                           message_form=message_form, db_sess=db_sess)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")



if __name__ == '__main__':
    db_session.global_init("orm/db/.db")
    # app.register_blueprint(jobs_api.blueprint)
    app.run(port=8080, host='127.0.0.1', debug=True)
