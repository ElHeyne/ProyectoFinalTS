# --- Fichero Principal --- #

# Importaciones
from flask import Flask, render_template, request, redirect, Response, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from functools import wraps
from models import Users
from werkzeug.security import generate_password_hash, check_password_hash
import db
import time
# import os
# import platform

# Definición / Rutas de Web

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)
# app.secret_key = os.environ.get("SECRET_KEY") or str(hash(platform.node())) # Sistema de session antiguo

@app.before_request
def validate_session():
    if request.endpoint == 'static':
        return
    print("DEBUG - Validando Sesion")
    time.sleep(0.3)
    print("DEBUG - Sesion Validada")
    if 'user_id' in session:
        user = db.session.query(Users).filter_by(user_id=session['user_id']).first()
        if not user:
            session.clear()
            flash("Error - Sesión Expirada", "warning")
            return redirect(url_for("login"))
        elif user.role_id != session.get('role_id'):
            session['role_id'] = user.role_id
            session['is_admin'] = user.role_id == 0

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
            return redirect(url_for('login'))

        user = db.session.query(Users).filter_by(user_id=session['user_id']).first()

        if not user or user.role_id != 0:
            print("Insufficient Roles")
            redirect_url = url_for('home')

        if redirect_url:
            return redirect(redirect_url)
        return original_function(*args, **kwargs)
    return decorated_function

# RUTAS SIN LOG IN

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")

# RUTAS USUARIO
@app.route("/")
@login_required
def home():
    return render_template("index.html", is_admin=session["is_admin"])

@app.route("/profile")
@login_required
def profile():
    return render_template("index_profile.html", is_admin=session["is_admin"])

@app.route("/products")
@login_required
def products():
    return render_template("index_products.html", is_admin=session["is_admin"])

@app.route("/statistics")
@login_required
def statistics():
    return render_template("index_statistics.html", is_admin=session["is_admin"])

# RUTAS ADMINISTRADOR

@app.route("/admin-panel")
@admin_login_required
def admin_panel():
    return render_template("admin.html", is_admin=session["is_admin"])

@app.route("/admin-panel/users")
@admin_login_required
def admin_panel_users():
    return render_template("admin_users.html", is_admin=session["is_admin"])

@app.route("/admin-panel/suppliers")
@admin_login_required
def admin_panel_suppliers():
    return render_template("admin_suppliers.html", is_admin=session["is_admin"])

@app.route("/admin-panel/products")
@admin_login_required
def admin_panel_products():
    return render_template("admin_products.html", is_admin=session["is_admin"])

@app.route("/admin-panel/categories")
@admin_login_required
def admin_panel_categories():
    return render_template("admin_categories.html", is_admin=session["is_admin"])

# RUTAS DE PROCESO

@app.route("/login-access", methods=["POST", "GET"])
def acceso_login():  # TODO Explicar en documentación
    template = "login.html"  # Default Template
    context = {"error_message": "Error Inesperado"}  # Default Mensaje

    if request.method == 'POST':
        _correo = request.form['txtEmail'].lower()
        _password = request.form['txtPassword']
        user = db.session.query(Users).filter_by(user_email=_correo).first()

        if user and user.verify_password(_password):  # Comprobación usuario activo y contraseña correcta
            session['user_id'] = user.user_id
            session['role_id'] = user.role_id
            session['login'] = True

            print("DEBUG - LOGGED IN", session)

            if session['role_id'] == 0:
                session['is_admin'] = True
                return redirect(url_for("admin_panel"))
            elif session['role_id'] == 1:
                session['is_admin'] = False
                return redirect(url_for("home"))
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
                     role_id=1)

        # Crear hash contraseña
        try:
            user.user_password = (request.form['txtPassword'])
        except Exception as e:
            print(e)
            context["error_message"] = "Error Proceso Hashing"

        # Revisar correo unico
        try:
            mail = request.form['txtEmail'].lower()

            if user.verify_mail(mail):
                flash("Advertencia: E-Mail Existente", "warning")
                return redirect(url_for("login"))
        except Exception as e:
            print(e)
            context["error_message"] = "Error Validar Mail"

        print(user)
        db.session.add(user)

        try:
            db.session.commit()
            flash("Usuario Creado", "success")
            return redirect(url_for("login"))

        except Exception as e:
            print(e)
            context["error_message"] = "Error Inseperado"

    return render_template(template, **context)


@app.route("/cerrar-login", methods=["POST", "GET"])
def cerrar_login():
    session.pop('user_id', None)
    session.pop('role_id', None)
    session.pop('is_admin', False)

    print("DEBUG - SESSIONS DELETED")

    return redirect(url_for("login"))


# Definimos un bucle if main para ejecutar la web
if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
    app.run(debug=True)
