from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField, FileField, SelectField
from wtforms.fields.html5 import EmailField, IntegerField
from wtforms.validators import DataRequired, Length


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(6, 30, "Неверное количество символов")])
    password_again = PasswordField('Повторите пароль',
                                   validators=[DataRequired(), Length(6, 30, "Неверное количество символов")])
    name = StringField('Имя пользователя', validators=[DataRequired(), Length(3, 30, "Неверное количество символов")])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class AddAnime_Form(FlaskForm):
    title_ru = StringField('Название', validators=[DataRequired()])
    title_jp = StringField('Оригинальное название', validators=[DataRequired()])
    ep_col = StringField('Количество эпизодов', validators=[DataRequired()])
    genres = StringField('Жанры (введите через запятую (Комедия,Школа,Ужасы))', validators=[DataRequired()])
    description = TextAreaField('Описание')
    dubs = StringField('Озвучки (вводить как и жанры)')
    release_year = IntegerField('Год выхода', validators=[DataRequired()])
    poster_path = FileField('Постер')
    submit = SubmitField('Добавить')


class Add_Dub_Genre_Form(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class Add_VideoForm(FlaskForm):
    dub = SelectField('Озвучка', validators=[DataRequired()])
    ep = StringField('Эпизод', validators=[DataRequired()])
    video = FileField('Видео', validators=[DataRequired()])
    ffmpeg_transcoding = BooleanField('Транскодировать в ffmpeg?')
    submit = SubmitField('Добавить')

    def __init__(self, dubs):
        super().__init__()
        self.dub.choices = [c.name for c in dubs]
