from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField, FileField
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
    image = FileField('Загрузите изображение', default='/static/img/default_image.jpg')
    submit = SubmitField('Зарегистрироваться')