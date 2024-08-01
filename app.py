from flask import Flask, render_template, request, session, redirect, url_for
from flask_mysqldb import MySQL
import config

app = Flask(__name__)

app.config['SECRET_KEY'] = config.HEX_SEC_KEY
app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB

mysql = MySQL(app)

@app.route('/', methods=['GET'])
def home():
    return render_template('main.html')

@app.route('/redirect', methods=['POST'])
def redirect_to_page():
    page = request.form.get('page')
    return redirect(url_for('render_page', page=page))

@app.route('/page/<page>')
def render_page(page):
    return render_template(f"{page}.html")

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s AND password= %s", (email, password))
    user = cur.fetchone()
    cur.close()

    if user is not None:
        session['email'] = email
        session['name'] = user[1]
        session['surname'] = user[2]

        return redirect(url_for('tasks'))
    else:
        return render_template('index.html', message="Las credenciales no son correctas")

@app.route('/tasks', methods=['GET'])
def tasks():
    return render_template('tasks.html')

if __name__ == '__main__':
    app.run(debug=True)