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
            return redirect(url_for('login'))
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

@app.route("/acceso-login", methods=["POST", "GET"])
def acceso_login():
    if request.method == 'POST':
        _correo = request.form['txtEmail']
        _password = request.form['txtPassword']
        print(_correo, _password)
        user=db.session.query(Users).filter_by(user_email=_correo).first()
        if user and _password == user.user_password:
            session['user_id'] = user.user_id
            return redirect(url_for("home"))
    return render_template("login.html", mensaje="Usuario Incorrecto")

@app.route("/cerrar-login", methods=["POST", "GET"])
def cerrar_login():
    session['user_id'] = None
    return render_template("login.html")

# Definimos un bucle if main para ejecutar la web
if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
    app.run(debug=True)