from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = StringField('Придумайте имя')
    uniq_name = StringField('Придумайте уникальный никнейм')
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль снова', validators=[DataRequired()])
    about = TextAreaField('Рассакажите о себе')
    vk_id = StringField(
        'ведите vk id')# (без @)
    submit = SubmitField('Reg')
