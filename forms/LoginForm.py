from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    user_auth_index = StringField('Введите ваш ник или VK_id (VK_id нужно вводить с @ в начале)',
                                  validators=[DataRequired()])
    password = PasswordField('Ведире пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')