# --- Fichero Principal --- #

# Importaciones
from flask import Flask, render_template, request, redirect, Response, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from functools import wraps
from models import Users
import db
import os
import platform

# Definición / Rutas de Web

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or str(hash(platform.node()))


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
        redirect_url = None
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
def acceso_login():  # TODO Explicar en documentación
    template = "login.html"  # Default Template
    context = {"error_message": "Error Inesperado"}  # Default Mensaje

    if request.method == 'POST':
        _correo = request.form['txtEmail'].lower()
        _password = request.form['txtPassword']
        user = db.session.query(Users).filter_by(user_email=_correo).first()

        if user and _password == user.user_password:  # Comprobación usuario activo y contraseña correcta
            session['user_id'] = user.user_id
            session['role_id'] = user.role_id
            session['login'] = True

            if session['role_id'] == 0:
                template = "admin.html"
            elif session['role_id'] == 1:
                template = "index.html"
            else:
                context["error_message"] = "Error de Privilegios"
        else:
            context["error_message"] = "Usuario Incorrecto"

    return render_template(template, **context)


@app.route("/register-access", methods=["POST", "GET"])
def acceso_registro():  # TODO Esplicar en documentacion (context con dos variables)
    template = "register.html"  # Default Template
    context = {"error_message": None, "success_message": None}  # Default Mensaje

    if request.method == 'POST':
        user = Users(user_name=request.form['txtUserName'],
                     user_email=request.form['txtEmail'].lower(),
                     user_password=request.form['txtPassword'],
                     role_id=1)
        print(user)
        db.session.add(user)

        try:
            db.session.commit()
            template = "login.html"
            context["success_message"] = "Usuario Creado"

        except:
            context["error_message"] = "Error Inseperado"

    return render_template(template, **context)


@app.route("/cerrar-login", methods=["POST", "GET"])
def cerrar_login():
    session.pop('user_id', None)
    session.pop('role_id', None)
    return redirect(url_for("login"))


# Definimos un bucle if main para ejecutar la web
if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
    app.run(debug=True)
