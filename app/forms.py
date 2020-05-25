from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateTimeField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class Search_params(FlaskForm):
    dt_start = DateTimeField("Дата и время начала мониторинга:",
                             validators=[DataRequired(message=None)])
    dt_finish = DateTimeField("Дата и время завершения мониторинга:",
                              validators=[DataRequired(message=None)])
    latitude = StringField("Широта:",
                           validators=[DataRequired(message=None)])
    longitude = StringField("Долгота:",
                            validators=[DataRequired(message=None)])
    submit = SubmitField("Отправить")
