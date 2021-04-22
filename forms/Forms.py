from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField, HiddenField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    uniq_name = StringField('Придумайте ник', validators=[DataRequired()])
    # если имя не будет введено, то парвметру name будет присвоен uniq_name
    name = StringField('Придумайте имя')
    password = PasswordField('Придумайте пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    about = TextAreaField('Рассакажите о себе')
    vk_id = StringField('Введите ваш VK_id (без @)')
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    user_auth_index = StringField('Введите ваш ник или VK_id (VK_id нужно вводить с @ в начале)',
                                  validators=[DataRequired()])
    password = PasswordField('Ведире пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')



class DiscussionForm(FlaskForm):
    discussion_title = StringField('Название обсуждения', validators=[DataRequired()])
    message = TextAreaField('Сообщение', validators=[DataRequired()])
    discussion_submit = SubmitField('Создать')


class ForumForm(FlaskForm):
    forum_title = StringField('Название форума', validators=[DataRequired()])
    forum_submit = SubmitField('Создать')


class MessageForm(FlaskForm):
    message = TextAreaField('Текст сообщения', validators=[DataRequired()])
    submit = SubmitField('Отправить')


class SearchForm(FlaskForm):
    search_field = StringField('Поиск', validators=[DataRequired()])
    submit = SubmitField('Искать')