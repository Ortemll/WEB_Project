from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired


class PhotoLoader(FlaskForm):
    image = FileField('Загрузите изображение')
    submit = SubmitField('Просмотреть изменения')
