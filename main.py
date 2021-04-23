from flask import *
from flask_login import login_user, login_required, LoginManager, logout_user, current_user, AnonymousUserMixin
from orm import db_session
from orm.__all_models import *
from forms.Forms import *
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


@app.route('/', methods=['GET', 'POST'])
def index():
    forum_form = ForumForm()
    discussion_form = DiscussionForm()
    db_sess = db_session.create_session()

    if request.method == 'POST':
        if request.form.get('delete_discussion'):
            delete_discussion(request.form['delete_discussion'], db_sess)
        elif request.form.get('delete_forum'):
            delete_forum(request.form['delete_forum'], db_sess)

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
            if True:
                pass  # чекаем вк id через бота вконтактееееееееееееееееееееееееееееееееееeeeeeeeeeeeeeeeeeeeeeee
            if db_sess.query(User).filter(User.vk_id == form.vk_id.data):
                return render_template('register.html', title='Регистрация', form=form,
                                       message="Пользователь с таким VK_id уже есть")

        user = User()
        user.uniq_name = form.uniq_name.data
        user.about = form.about.data
        user.vk_id = form.vk_id.data if form.vk_id.data else None
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


@app.route('/discussion/<int:id>', methods=['GET', 'POST'])
def discussion(id):
    db_sess = db_session.create_session()
    message_form = MessageForm()

    if current_user.is_authenticated:
        local_current_user = db_sess.query(User).get(current_user.id)  # чтобы небыло проблем с сессиями

    if request.method == 'POST':
        if request.form.get('edit_id'):
            message = db_sess.query(Message).get(request.form['edit_id'])
            message.content = request.form['edited_message']
            db_sess.commit()
        if request.form.get('delete_comment'):
            for comment in db_sess.query(Message).filter(
                    Message.answers_to_id == request.form['delete_comment']).all():
                comment.answers_to_id = None
                db_sess.merge(comment)
            db_sess.delete(db_sess.query(Message).get(request.form['delete_comment']))
            db_sess.commit()

        elif request.form.get('like'):
            liked_mess = db_sess.query(Message).get(request.form['like'])
            if liked_mess not in local_current_user.liked:
                if liked_mess in local_current_user.disliked:
                    local_current_user.disliked.remove(liked_mess)
                    liked_mess.dislikes -= 1
                liked_mess.likes += 1
                local_current_user.liked.append(liked_mess)
                print(liked_mess.likes == len(liked_mess.liked_by))
            else:
                local_current_user.liked.remove(liked_mess)
                liked_mess.likes -= 1
            db_sess.commit()
        elif request.form.get('dislike'):
            disliked_mess = db_sess.query(Message).get(request.form['dislike'])
            if disliked_mess not in local_current_user.disliked:
                if disliked_mess in local_current_user.liked:
                    local_current_user.liked.remove(disliked_mess)
                    disliked_mess.likes -= 1
                local_current_user.disliked.append(disliked_mess)
                disliked_mess.dislikes += 1
            else:
                local_current_user.disliked.remove(disliked_mess)
                disliked_mess.dislikes -= 1
            db_sess.commit()

    discussion = db_sess.query(Discussion).get(id)
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
                           message_form=message_form, db_sess=db_sess,
                           sorted=sorted, key=lambda el: el.date)


@app.route('/user/<int:id>', methods=['GET', 'POST'])
def user(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(id)
    if not user:
        return redirect('/')

    if request.method == 'POST':
        if request.form.get('set_admin'):
            user.lvl = 1 if int(request.form['set_admin']) else 2
            db_sess.commit()
        elif request.form.get('ban_user'):
            print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', request.form['ban_user'])
            user.is_banned = bool(int(request.form['ban_user'])) # aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
            user.lvl = 2
            db_sess.commit()
        elif request.form.get('delete_user'):
            for discussion in user.discussions:
                delete_discussion(discussion.id, db_sess)
            for forum in user.forums:
                delete_forum(forum.id, db_sess)
            db_sess.delete(user)
            db_sess.commit()
            return redirect('/')
        elif request.form.get('edit_user'):
            pass  # wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww

    return render_template('user.html', user=user, max=max, len=len)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def delete_forum(id, db_sess):
    forum_to_delete = db_sess.query(Forum).get(id)
    for disc_to_delete in forum_to_delete.discussions:
        delete_discussion(disc_to_delete.id, db_sess)
    db_sess.delete(forum_to_delete)
    db_sess.commit()


def delete_discussion(id, db_sess):
    disc_to_delete = db_sess.query(Discussion).get(id)
    for message in disc_to_delete.messages:
        db_sess.delete(message)
    db_sess.delete(disc_to_delete)
    db_sess.commit()


if __name__ == '__main__':
    db_session.global_init("orm/db/.db")
    # app.register_blueprint(jobs_api.blueprint)
    app.run(port=8080, host='127.0.0.1', debug=True)
