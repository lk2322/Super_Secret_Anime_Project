from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Главная страница', new_anime=[{'name':'123'}, {'name':'143'}])


app.run('127.0.0.1', 8081, debug=True)
