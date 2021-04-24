import datetime
import os
import pathlib

from flask import Flask, render_template, redirect, url_for, request, Response, g, abort
from sqlalchemy import desc, func

from add_video import save_video
from config import Config
from data.genres import Genres
from utils.id_gen import id_generator

from data import db_session
from data.anime import Anime
from data.roles import Roles
from data.users import User
from data.dubs import Dubs
from forms import RegisterForm, LoginForm, AddAnime_Form, Add_Dub_Genre_Form, Add_VideoForm
from blueprints import get_video
from flask_login import LoginManager, login_user, current_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.secret_key
db_session.global_init("main.db")
app.register_blueprint(get_video.blueprint)
login_manager = LoginManager()
login_manager.init_app(app)


def check_admin(user):
    if user.is_anonymous:
        return False
    db_sess = db_session.create_session()
    role = db_sess.query(Roles).filter(Roles.name == 'Admin').first()
    c_user = db_sess.merge(user)
    if role in c_user.roles:
        db_sess.close()
        return True


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    db_sess.close()
    return user


@app.errorhandler(404)
def not_auth_error(e):
    return render_template('error.html', message='Такой страницы не существует')


@app.route('/')
@app.route('/index')
def index():
    db_sess = db_session.create_session()
    new_anime = db_sess.query(Anime).order_by(desc(Anime.created_date)).limit(5).all()
    updated_anime = db_sess.query(Anime).order_by(desc(Anime.modified_date)).limit(5).all()
    db_sess.close()

    return render_template('index.html', title='Главная страница', new_anime=new_anime, update_anime=updated_anime)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Этот email уже используется. У вас уже есть аккаунт?")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        db_sess.close()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/search')
def search():
    query = request.args.get('q')
    q_genre = request.args.get('genre')
    q_dub = request.args.get('dub')
    db_sess = db_session.create_session()
    res = db_sess.query(Anime).filter(
        (Anime.title_ru.ilike(f'%{query}%')) | (Anime.title_jp.ilike(f'%{query}%')) | (Anime.dubs.any(name=q_dub)) | (
            Anime.genres.any(name=q_genre)))
    db_sess.close()
    title = []
    if query:
        title.append(query)
    if q_dub:
        title.append(q_dub)
    if q_genre:
        title.append(q_genre)
    return render_template('search.html', res=res, title=f'Поиск: {", ".join(title)}', query=title)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            db_sess.close()
            return redirect("/")
        db_sess.close()
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/profile')
def profile():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        fav = db_sess.query(User).filter(User.id == current_user.id).first().favorites
        db_sess.close()
        return render_template('profile.html', fav=fav, is_admin=check_admin(current_user), title='Закладки')
    return render_template('error.html', message='Недостаточно прав'), 401


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if check_admin(current_user):
        form = Add_Dub_Genre_Form()
        form2 = AddAnime_Form()
        if request.method == 'GET':
            return render_template('admin.html', form=form, form2=form2, title='Админка')
        if request.method == 'POST':
            if form2.validate_on_submit():
                add_edit_anime(form2, False)
                return redirect('/admin')
            if form.validate_on_submit():
                db_sess = db_session.create_session()
                dub = Dubs(name=form.name.data)
                db_sess.add(dub)
                db_sess.commit()
                db_sess.close()
                return redirect('/admin')

    return render_template('error.html', message='Недостаточно прав'), 401


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect('/')
    return render_template('error.html', message='Недостаточно прав'), 401


@app.route('/random_anime')
def random_anime():
    db_sess = db_session.create_session()
    anime_id = db_sess.query(Anime).order_by(func.random()).limit(1).first().id
    db_sess.close()
    return redirect(url_for('anime', anime_id=anime_id))


def add_genre_to_db(name: str, db_sess):
    """Нужно передать db_session, а после самому закрыть"""
    genre = Genres(name=name)
    db_sess.add(genre)
    db_sess.commit()


def add_edit_anime(form, edit: bool, anime_id: int = 0):
    """Если edit == False, то anime_id не нужно"""
    db_sess = db_session.create_session()
    if edit:
        anime = db_sess.query(Anime).filter(Anime.id == anime_id).first()
    else:
        anime = Anime()
    anime.title_ru = form.title_ru.data
    anime.title_jp = form.title_jp.data
    anime.ep_col = form.ep_col.data
    anime.description = form.description.data
    anime.release_year = form.release_year.data
    if form.genres.data:
        genres = form.genres.data.split(',')
        for i in genres:
            genre = db_sess.query(Genres).filter(Genres.name == i).first()
            if not genre:
                add_genre_to_db(i, db_sess)
                genre = db_sess.query(Genres).filter(Genres.name == i).first()
            anime.genres.append(genre)
    if form.dubs.data:
        dubs = form.dubs.data.split(',')
        for i in dubs:
            dub = db_sess.query(Dubs).filter(Dubs.name == i).first()
            if dub:
                anime.dubs.append(dub)
    if form.description.data:
        anime.description = form.description.data
    else:
        anime.description = ''
    if form.poster_path.data:
        _, filename = os.path.splitext(form.poster_path.data.filename)
        name = id_generator() + filename
        path = os.path.join(app.static_folder, 'img', 'posters', name)
        form.poster_path.data.save(path)
        # Костыль
        anime.poster_path = 'static/' + 'img/' + 'posters/' + name
    if not edit:
        db_sess.add(anime)
    db_sess.commit()
    db_sess.close()


@app.route('/anime/<int:anime_id>/edit_anime', methods=['GET', 'POST'])
def edit_anime(anime_id):
    if request.method == 'GET':
        if check_admin(current_user):
            db_sess = db_session.create_session()
            anime = db_sess.query(Anime).filter(Anime.id == anime_id).first()
            form = AddAnime_Form(obj=anime)
            form.dubs.data = ','.join([i.name for i in anime.dubs])
            form.genres.data = ','.join([i.name for i in anime.genres])
            db_sess.close()
            return render_template('edit_anime.html', form=form)
    elif request.method == 'POST':
        if check_admin(current_user):
            form = AddAnime_Form()
            if form.validate_on_submit():
                add_edit_anime(form, True, anime_id)
    return render_template('error.html', message='Недостаточно прав'), 401


@app.route('/anime/<int:anime_id>/add_video', methods=['GET', 'POST'])
def add_video(anime_id):
    if check_admin(current_user):
        db_sess = db_session.create_session()
        anime = db_sess.query(Anime).filter(Anime.id == anime_id).first()
        dubs = anime.dubs
        if request.method == 'GET':
            form = Add_VideoForm(dubs)
            db_sess.close()
            return render_template('add_video.html', form=form)
        if request.method == 'POST':
            form = Add_VideoForm(dubs)
            if form.validate_on_submit():
                path = save_video(anime_id, form.ep.data, form.dub.data, form.video.data, form.ffmpeg_transcoding.data)
                anime.videos_path = path
                anime.modified_date = datetime.datetime.now()
                db_sess.commit()
            return redirect('/')
        db_sess.close()
    return render_template('error.html', message='Недостаточно прав'), 401


@app.route('/anime/<int:anime_id>/video_info')
def video_info(anime_id):
    return redirect(url_for('static', filename=fr'video/{anime_id}/info.json'))


@app.route('/anime/<int:anime_id>/bookmark', methods=['GET', 'POST', 'DELETE'])
def bookmark(anime_id):
    """При запросе возвращает 400 код, если аниме уже в закладках
        При post запросе добавляет в закладки, если его нет в них"""
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        anime = db_sess.query(Anime).filter(Anime.id == anime_id).first()
        if anime in user.favorites:
            if request.method == 'DELETE':
                user.favorites.remove(anime)
                db_sess.commit()
                db_sess.close()
                return 'Deleted'
            return Response('Anime already in favorites', 400)
        if request.method == 'POST':
            user.favorites.append(anime)
            db_sess.commit()
            db_sess.close()
            return 'Added'
        return 'Not in bookmarks'
    return render_template('error.html', message='Недостаточно прав'), 401


@app.route('/anime/<int:anime_id>')
def anime(anime_id: int):
    db_sess = db_session.create_session()
    anime = db_sess.query(Anime).filter(Anime.id == anime_id).first()
    dubs = anime.dubs
    genres = anime.genres
    is_admin = check_admin(current_user)
    db_sess.close()
    return render_template('anime.html', anime=anime, dubs=dubs, genres=genres, is_admin=is_admin, title=anime.title_ru)


def init():
    pathlib.Path('static/img/posters').mkdir(parents=True, exist_ok=True)
    pathlib.Path('static/video').mkdir(parents=True, exist_ok=True)
    pathlib.Path('temp').mkdir(parents=True, exist_ok=True)
    db_sess = db_session.create_session()
    if not db_sess.query(Roles).filter(Roles.name == 'Admin').first():
        role = Roles(name='Admin')
        db_sess.add(role)
    else:
        role = db_sess.query(Roles).filter(Roles.name == 'Admin').first()
    for i in Config.admins:
        user = db_sess.query(User).filter(User.id == i).first()
        if user:
            if role not in user.roles:
                user.roles.append(role)
    # TODO забирать админки у отсутсвующих в конфиге id
    db_sess.commit()
    db_sess.close()


if __name__ == "__main__":
    init()
    app.run(Config.ip, Config.port, threaded=True)
