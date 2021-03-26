from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from forms import RegisterForm, LoginForm
from blueprints import get_video
from flask_login import LoginManager, login_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sadasd'
db_session.global_init("D:\projects\Super_Secret_Anime_Project\db\main.db")
app.register_blueprint(get_video.blueprint)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Главная страница', new_anime=[{'name': '123'}, {'name': '143'}])


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
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


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
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


if __name__ == "__main__":
    app.run('127.0.0.1', 8081, debug=True, threaded=True)
