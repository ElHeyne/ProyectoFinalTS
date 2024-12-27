# --- Fichero Principal --- #

# Importaciones
from flask import Flask, render_template, request, redirect, Response, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from functools import wraps
from models import Users
import db

# Definición / Rutas de Web

app = Flask(__name__)
app.secret_key = "TS_EVVH_2024" # TODO crear clave segura y aleatoria usando .env


def login_required(original_function):
    @wraps(original_function)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            print("Not Logged In")
            return redirect(url_for('login'))
        return original_function(*args, **kwargs)
    return decorated_function

def admin_login_required(original_function):
    @wraps(original_function)
    def decorated_function(*args, **kwargs):
        redirect_url=None
        if 'user_id' not in session:
            print("Not Logged In")
            redirect_url = url_for('login')
        elif session['role_id'] != 0:
            print("Insuficient Roles")
            redirect_url = url_for('home')

        if redirect_url:
            return redirect(redirect_url)
        return original_function(*args, **kwargs)
    return decorated_function

# # Ruta Main
@app.route("/")
@login_required
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/admin-panel")
@admin_login_required
def admin_panel():
    return render_template("admin.html")

@app.route("/login-access", methods=["POST", "GET"])
def acceso_login(): # TODO optimizar los returns aplicando variable de url y de mensaje
    if request.method == 'POST':
        _correo = request.form['txtEmail']
        _password = request.form['txtPassword']
        user=db.session.query(Users).filter_by(user_email=_correo).first()
        if user and _password == user.user_password:
            session['user_id'] = user.user_id
            session['role_id'] = user.role_id
            session['login'] = True
            if session['role_id']==0:
                return redirect(url_for("admin_panel"))
            elif session['role_id']==1:
                return redirect(url_for("home"))
            else:
                return render_template("login.html", error_message="Error de Privilegios")
    return render_template("login.html", error_message="Usuario Incorrecto")

@app.route("/register-access", methods=["POST", "GET"])
def acceso_registro(): # TODO optimizar los returns aplicando variable de url y de mensaje
    if request.method == 'POST':
        user = Users(user_name=request.form['txtUserName'], user_email=request.form['txtEmail'], user_password=request.form['txtPassword'], role_id=1)
        print(user)
        db.session.add(user)
        db.session.commit()
        return render_template("login.html", success_message="Usuario Creado")
    return render_template("register.html", error_message="Error de Endpoint")

@app.route("/cerrar-login", methods=["POST", "GET"])
def cerrar_login():
    session.pop('user_id',None)
    session.pop('role_id', None)
    return redirect(url_for("login"))

# Definimos un bucle if main para ejecutar la web
if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
    app.run(debug=True)