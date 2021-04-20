from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    uniq_name = StringField('Придумайте ник', validators=[DataRequired()])
    # если имя не будет введено, то парвметру name будет присвоен uniq_name
    name = StringField('Придумайте имя')
    uniq_name = StringField('Придумайте уникальный никнейм', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль снова', validators=[DataRequired()])
    about = TextAreaField('Рассакажите о себе')
    vk_id = StringField('Введите ваш VK_id (без @)')
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Зарегистрироваться')