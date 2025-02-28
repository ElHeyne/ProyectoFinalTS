# --- Fichero Principal --- #

# Importaciones
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
from functools import wraps
from models import Users, Suppliers, Categories, Products, Roles
from sqlalchemy import case, desc, label, func
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
    time.sleep(0.3)
    if 'user_id' in session:
        user = db.session.query(Users).filter_by(user_id=session['user_id']).first()
        if not user:
            session.clear()
            flash("Sesión Expirada", "warning")
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
    user_name = session['user_name']
    return render_template("index.html", is_admin=session["is_admin"],
                           user_name=user_name)


@app.route("/profile")
@login_required
def profile():
    user_id = session['user_id']
    role_id = session['role_id']

    user_name = session['user_name']

    user_role = db.session.query(Roles).filter_by(role_id=role_id).first()
    user = db.session.query(Users).filter_by(user_id=user_id).first()
    return render_template("index_profile.html", is_admin=session["is_admin"],
                           user_name=user_name,
                           user_role=user_role,
                           active_user=user)


@app.route("/products")
@login_required
def products():
    public_products = db.session.query(
        Suppliers.supplier_name,
        Categories.category_name,
        Products.product_name,
        Products.product_selling_price,
        Products.product_referencial,
        Products.product_limit_stock,
        Products.product_active_stock,
        Products.product_description,
    ).join(Suppliers, Products.supplier_id == Suppliers.supplier_id).join(Categories, Products.category_id == Categories.category_id)

    most_demanded_products = db.session.query(
        Products.product_name,
        label(
            "ventas",
            (Products.product_limit_stock - Products.product_active_stock)
        )
    ).where(
        (Products.product_limit_stock - Products.product_active_stock) > (db.session.query((func.avg(label("ventas",(Products.product_limit_stock - Products.product_active_stock))))/5))
    ).order_by(
        label("ventas", (Products.product_limit_stock - Products.product_active_stock)).desc()
    ).limit(10)

    return render_template("index_products.html", is_admin=session["is_admin"],
                           public_products=public_products,
                           most_demanded_products=most_demanded_products)


@app.route("/statistics")
@login_required
def statistics():
    # Estadistica de productos con mas ventas
    most_demanded_products = db.session.query(
        Products.product_name,
        label(
            "ventas",
            (Products.product_limit_stock - Products.product_active_stock)
        )
    ).order_by(
        label("ventas", (Products.product_limit_stock - Products.product_active_stock)).desc()
    ).limit(10)

    # Estadistica de proveedores con mas productos
    most_popular_suppliers = db.session.query(
        Suppliers.supplier_name,
        label(
            "productos",
            func.count(Products.product_name)
        )
    ).join(
        Products, Products.supplier_id == Suppliers.supplier_id
    ).order_by(
        label("productos", func.count(Products.product_name)).desc()
    ).group_by(
        Suppliers.supplier_name
    ).limit(10)

    # Estadistica de categorias con mas productos
    most_popular_categories = db.session.query(
        Categories.category_name,
        label(
            "productos",
            func.count(Products.product_name)
        )
    ).join(
        Products, Products.category_id == Categories.category_id
    ).order_by(
        label("productos", func.count(Products.product_name)).desc()
    ).group_by(
        Categories.category_name
    ).limit(10) # TODO Ajustar altura de lineas

    return render_template("index_statistics.html", is_admin=session["is_admin"],
                           most_demanded_products=most_demanded_products,
                           most_popular_suppliers=most_popular_suppliers,
                           most_popular_categories=most_popular_categories)


# RUTAS ADMINISTRADOR


@app.route("/admin-panel")
@admin_login_required
def admin_panel():
    total_registered_users = db.session.query(
        label(
            "total",
            func.count(Users.user_id)
        ),
        label(
            "users",
            func.count(case((Users.role_id == 1, 1)))
        ),
        label(
            "admins",
            func.count(case((Users.role_id == 0, 1)))
        )
    )

    most_sold_products = db.session.query(
        Products.product_name,
        label(
            "sales",
            (Products.product_limit_stock - Products.product_active_stock)
        )
    ).order_by(
        label("sales", (Products.product_limit_stock - Products.product_active_stock)).desc()
    ).limit(10)

    most_critical_stock_products = db.session.query(
        Products.product_name,
        label(
            "product_stock",
            func.round((100 * (Products.product_active_stock/Products.product_limit_stock)), 2)
        )
    ).order_by(
        label("product_stock", func.round((100 * (Products.product_active_stock/Products.product_limit_stock)), 2))
    ).filter(
        label("product_stock", func.round((100 * (Products.product_active_stock/Products.product_limit_stock)), 2)) < 90
    ).limit(10)

    products_without_stock = db.session.query(
        Products.product_name
    ).filter(
        Products.product_active_stock == 0
    ).scalar()

    most_negative_profit_products = db.session.query(
        Products.product_name,
        label(
            "product_profit",
            func.round((100 * ((Products.product_selling_price / Products.product_price) - 1)), 2)
        )
    ).filter(
        label("product_profit",func.round((100 * ((Products.product_selling_price / Products.product_price) - 1)), 2)) < 0
    ).order_by(
        label("product_profit",func.round((100 * ((Products.product_selling_price / Products.product_price) - 1)), 2)).desc()
    ).limit(10)

    most_popular_suppliers = db.session.query(
        Suppliers.supplier_name,
        label(
            "product_count",
            func.count(Products.product_name)
        )
    ).join(
        Products, Products.supplier_id == Suppliers.supplier_id
    ).order_by(
        label("productos", func.count(Products.product_name)).desc()
    ).group_by(
        Suppliers.supplier_name
    ).having(
        label("productos", func.count(Products.product_name)) > 0
    ).limit(10).all()

    most_discounted_suppliers = db.session.query(
        Suppliers.supplier_name,
        Suppliers.supplier_discount
    ).order_by(
        Suppliers.supplier_discount.desc()
    ).filter(
        Suppliers.supplier_discount > 0
    ).limit(10).all()

    most_popular_categories = db.session.query(
        Categories.category_name,
        label(
            "product_count",
            func.count(Products.product_name)
        )
    ).join(
        Products, Products.category_id == Categories.category_id
    ).order_by(
        label("productos", func.count(Products.product_name)).desc()
    ).group_by(
        Categories.category_name
    ).having(
        label("productos", func.count(Products.product_name)) > 0
    ).limit(10).all()

    categories_without_products = db.session.query(
        Categories.category_name,
        label(
            "product_count",
            func.count(Products.product_name)
        )
    ).join(
        Products, Products.category_id == Categories.category_id
    ).order_by(
        label("productos", func.count(Products.product_name)).desc()
    ).group_by(
        Categories.category_name
    ).having(
        label("productos", func.count(Products.product_name)) == 0
    ).limit(10).all()

    return render_template("admin.html", is_admin=session["is_admin"],
                           total_registered_users=total_registered_users,
                           most_sold_products=most_sold_products,
                           most_critical_stock_products=most_critical_stock_products,
                           products_without_stock=products_without_stock,
                           most_negative_profit_products=most_negative_profit_products,
                           most_popular_suppliers=most_popular_suppliers,
                           most_popular_categories=most_popular_categories,
                           categories_without_products=categories_without_products,
                           most_discounted_suppliers=most_discounted_suppliers)


@app.route("/admin-panel/users")
@admin_login_required
def admin_panel_users():
    registered_users = db.session.query(Users).order_by(Users.user_id)
    recent_registers = db.session.query(Users).order_by(desc(Users.user_register_date)).limit(5)
    return render_template("admin_users.html", is_admin=session["is_admin"],
                           registered_users=registered_users,
                           recent_registers=recent_registers)


@app.route("/admin-panel/users/confirm-deletion/<int:delete_id>", methods=["POST", "GET"])
@admin_login_required
def admin_panel_users_confirm_deletion(delete_id):
    user = db.session.query(Users).filter_by(user_id=delete_id).first()

    if request.method == "POST":
        if "confirm" in request.form:
            try:
                db.session.query(Users).filter_by(user_id=delete_id).delete()
                db.session.commit()
                flash(f"Eliminado Usuario {user.user_id} - {user.user_name}", "success")
                return redirect(url_for("admin_panel_users"))
            except Exception as e:
                print(e)
                flash("Error Proceso Eliminación Usuario", "error")
                return redirect(url_for("admin_panel_users"))
        elif "cancel" in request.form:
            flash("Eliminación Cancelada", "warning")
            return redirect(url_for("admin_panel_users"))

    return render_template("admin_users_confirm_deletion.html", user=user, is_admin=session["is_admin"])


@app.route("/admin-panel/suppliers")
@admin_login_required
def admin_panel_suppliers():
    registered_suppliers = db.session.query(Suppliers).order_by(Suppliers.supplier_id)
    return render_template("admin_suppliers.html", is_admin=session["is_admin"],
                           registered_suppliers=registered_suppliers)


@app.route("/admin-panel/suppliers/confirm-deletion/<int:delete_id>", methods=["POST", "GET"])
@admin_login_required
def admin_panel_suppliers_confirm_deletion(delete_id):
    supplier = db.session.query(Suppliers).filter_by(supplier_id=delete_id).first()

    if request.method == "POST":
        if "confirm" in request.form:
            try:
                db.session.query(Suppliers).filter_by(supplier_id=delete_id).delete()
                db.session.commit()
                flash(f"Eliminado Proveedor {supplier.supplier_id} - {supplier.supplier_name}", "success")
                return redirect(url_for("admin_panel_suppliers"))
            except Exception as e:
                print(e)
                flash("Error Proceso Eliminación Proveedor", "error")
                return redirect(url_for("admin_panel_suppliers"))
        elif "cancel" in request.form:
            flash("Eliminación Cancelada", "warning")
            return redirect(url_for("admin_panel_suppliers"))

    return render_template("admin_suppliers_confirm_deletion.html", supplier=supplier, is_admin=session["is_admin"])


@app.route("/admin-panel/products")
@admin_login_required
def admin_panel_products():
    registered_products = db.session.query(
        Products.product_id,
        Suppliers.supplier_name,
        Categories.category_name,
        Products.product_name,
        Products.product_price,
        Products.product_selling_price,
        Products.product_referencial,
        Products.product_limit_stock,
        Products.product_active_stock,
        Products.product_warehouse,
        Products.product_zone,
        Products.product_description,
        label(
            "product_profit",
            func.round((100 * ((Products.product_selling_price / Products.product_price) - 1)), 2)
        )
    ).join(Suppliers, Products.supplier_id == Suppliers.supplier_id).join(Categories, Products.category_id == Categories.category_id)

    registered_categories = db.session.query(Categories).order_by(Categories.category_id)

    registered_suppliers = db.session.query(Suppliers).order_by(Suppliers.supplier_id)

    return render_template("admin_products.html", is_admin=session["is_admin"],
                           registered_products=registered_products,
                           registered_categories=registered_categories,
                           registered_suppliers=registered_suppliers)


@app.route("/admin-panel/products/confirm-deletion/<int:delete_id>", methods=["POST", "GET"])
@admin_login_required
def admin_panel_products_confirm_deletion(delete_id):
    product = db.session.query(Products).filter_by(product_id=delete_id).first()

    if request.method == "POST":
        if "confirm" in request.form:
            try:
                db.session.query(Products).filter_by(product_id=delete_id).delete()
                db.session.commit()
                flash(f"Eliminada Categoría {product.product_id} - {product.product_name} - {product.product_referencial}", "success")
                return redirect(url_for("admin_panel_products"))
            except Exception as e:
                print(e)
                flash("Error Proceso Eliminación Producto", "error")
                return redirect(url_for("admin_panel_products"))
        elif "cancel" in request.form:
            flash("Eliminación Cancelada", "warning")
            return redirect(url_for("admin_panel_products"))

    return render_template("admin_products_confirm_deletion.html", product=product, is_admin=session["is_admin"])


@app.route("/admin-panel/categories")
@admin_login_required
def admin_panel_categories():
    registered_categories = db.session.query(Categories).order_by(Categories.category_id)
    return render_template("admin_categories.html", is_admin=session["is_admin"],
                           registered_categories=registered_categories)


@app.route("/admin-panel/categories/confirm-deletion/<int:delete_id>", methods=["POST", "GET"])
@admin_login_required
def admin_panel_categories_confirm_deletion(delete_id):
    category = db.session.query(Categories).filter_by(category_id=delete_id).first()

    if request.method == "POST":
        if "confirm" in request.form:
            try:
                db.session.query(Categories).filter_by(category_id=delete_id).delete()
                db.session.commit()
                flash(f"Eliminada Categoría {category.category_id} - {category.category_name}", "success")
                return redirect(url_for("admin_panel_categories"))
            except Exception as e:
                print(e)
                flash("Error Proceso Eliminación Categoría", "error")
                return redirect(url_for("admin_panel_categories"))
        elif "cancel" in request.form:
            flash("Eliminación Cancelada", "warning")
            return redirect(url_for("admin_panel_categories"))

    return render_template("admin_categories_confirm_deletion.html", category=category, is_admin=session["is_admin"])


# RUTAS DE PROCESO


@app.route("/login-access", methods=["POST", "GET"])
def acceso_login():
    if request.method == 'POST':
        _correo = request.form['txtEmail'].lower()
        _password = request.form['txtPassword']
        user = db.session.query(Users).filter_by(user_email=_correo).first()

        # Comprobación usuario activo y contraseña correcta
        if user and user.verify_password(_password):
            session['user_name'] = user.user_name
            session['user_id'] = user.user_id
            session['role_id'] = user.role_id
            session['login'] = True

            if session['role_id'] == 0:
                session['is_admin'] = True
                return redirect(url_for("admin_panel"))
            elif session['role_id'] == 1:
                session['is_admin'] = False
                return redirect(url_for("home"))
            else:
                flash("Error de Privilegios", "error")
                return redirect(url_for("login"))
        else:
            flash("Contraseña Incorrecto", "error")
            return redirect(url_for("login"))

    flash("Error de Método", "error")
    return redirect(url_for("login"))


@app.route("/register-access", methods=["POST", "GET"])
def acceso_registro():
    if request.method == 'POST':
        user = Users(user_name=request.form['txtUserName'],
                     user_email=request.form['txtEmail'].lower(),
                     role_id=1)

        # Crear hash contraseña
        try:
            user.user_password = (request.form['txtPassword'])
        except Exception as e:
            print(e)
            flash("Error Proceso Hashing", "error")
            return redirect(url_for("login"))

        # Revisar correo unico
        try:
            mail = request.form['txtEmail'].lower()

            if user.verify_mail(mail):
                flash("E-Mail Existente", "warning")
                return redirect(url_for("login"))
        except Exception as e:
            print(e)
            flash("Error Validar Mail", "error")
            return redirect(url_for("login"))

        # Añadir usuario
        try:
            db.session.add(user)
            db.session.commit()
            flash("Usuario Creado", "success")
            return redirect(url_for("login"))

        except Exception as e:
            print(e)
            flash("Error Procesar Usuario", "error")
            return redirect(url_for("login"))

    flash("Error de Método", "error")
    return redirect(url_for("login"))


@app.route("/cerrar-login", methods=["POST", "GET"])
def cerrar_login():
    session.pop('user_name', None)
    session.pop('user_id', None)
    session.pop('role_id', None)
    session.pop('is_admin', False)

    flash("Sessión Cerrada", "warning")
    return redirect(url_for("login"))


@app.route("/admin-panel/users/add-user", methods=["POST", "GET"])
def admin_panel_users_add_user():
    if request.method == 'POST':
        user = Users(user_name=request.form['txtUserName'],
                     user_email=request.form['txtEmail'].lower(),
                     role_id=int(request.form['txtRole']))

        # Crear hash contraseña
        try:
            user.user_password = (request.form['txtPassword'])
        except Exception as e:
            print(e)
            flash("Error Proceso Hashing", "error")
            return redirect(url_for("admin_panel_users"))

        # Revisar correo unico
        try:
            mail = request.form['txtEmail'].lower()

            if user.verify_mail(mail):
                flash("E-Mail Existente", "warning")
                return redirect(url_for("admin_panel_users"))
        except Exception as e:
            print(e)
            flash("Error Validar Mail", "error")
            return redirect(url_for("admin_panel_users"))

        # Añadir usuario
        try:
            db.session.add(user)
            db.session.commit()
            flash("Usuario Creado", "success")
            return redirect(url_for("admin_panel_users"))

        except Exception as e:
            print(e)
            flash("Error Procesar Usuario", "error")
            return redirect(url_for("admin_panel_users"))

    flash("Error de Método", "error")
    return redirect(url_for("admin_panel_users"))


@app.route("/admin-panel/users/delete-user/<int:delete_id>", methods=["POST"])
def admin_panel_users_delete_user(delete_id):
    if request.method == 'POST':
        if isinstance(delete_id, int):
            return redirect(url_for("admin_panel_users_confirm_deletion", delete_id=delete_id))
        else:
            flash("Error de ID", "error")
            return redirect(url_for("admin_panel_users"))

    flash("Error de Método", "error")
    return redirect(url_for("admin_panel_users"))


@app.route("/admin-panel/suppliers/add-supplier", methods=["POST", "GET"])
def admin_panel_suppliers_add_supplier():
    if request.method == "POST":
        supplier = Suppliers(supplier_name=request.form['txtSupplierName'],
                             supplier_phone=request.form['txtSupplierPhone'],
                             supplier_nif=request.form['txtSupplierNif'].upper(),
                             supplier_commercial_address=request.form['txtSupplierAddress'],
                             supplier_discount=request.form['txtSupplierDiscount'],
                             supplier_iva=request.form['txtSupplierIva'],
                             supplier_country=request.form['txtSupplierCountry'])
        
        # Revisar Nombre Único
        try:
            name = request.form['txtSupplierName'].lower()

            if supplier.verify_name(name):
                flash("Nombre de Proveedor Existente", "warning")
                return redirect(url_for("admin_panel_suppliers"))
        except Exception as e:
            print(e)
            flash("Error Validar Nombre", "error")
            return redirect(url_for("admin_panel_suppliers"))

        # Revisar Teléfono Único
        try:
            phone = request.form['txtSupplierPhone']

            if supplier.verify_phone(phone):
                flash("Número de Proveedor Existente", "warning")
                return redirect(url_for("admin_panel_suppliers"))
        except Exception as e:
            print(e)
            flash("Error Validar Número", "error")
            return redirect(url_for("admin_panel_suppliers"))

        # Revisar NIF Único
        try:
            nif = request.form['txtSupplierNif'].upper()

            if supplier.verify_nif(nif):
                flash("NIF de Proveedor Existente", "warning")
                return redirect(url_for("admin_panel_suppliers"))
        except Exception as e:
            print(e)
            flash("Error Validar NIF", "error")
            return redirect(url_for("admin_panel_suppliers"))

        # Añadir proveedor
        try:
            db.session.add(supplier)
            db.session.commit()
            flash("Proveedor Creado", "success")
            return redirect(url_for("admin_panel_suppliers"))

        except Exception as e:
            print(e)
            flash("Error Procesar Proveedor", "error")
            return redirect(url_for("admin_panel_suppliers"))


@app.route("/admin-panel/suppliers/delete-supplier/<int:delete_id>", methods=["POST"])
def admin_panel_suppliers_delete_supplier(delete_id):
    if request.method == 'POST':
        if isinstance(delete_id, int):
            return redirect(url_for("admin_panel_suppliers_confirm_deletion", delete_id=delete_id))
        else:
            flash("Error de ID", "error")
            return redirect(url_for("admin_panel_suppliers"))

    flash("Error de Método", "error")
    return redirect(url_for("admin_panel_suppliers"))


@app.route("/admin-panel/categories/add-category", methods=["POST", "GET"])
def admin_panel_categories_add_category():
    if request.method == 'POST':
        category = Categories(category_name=request.form['txtCategoryName'],
                              category_referencial=request.form['txtCategoryReferencial'].upper(),
                              category_zone=request.form['txtCategoryZone'].upper())

        # Revisar Nombre Unico
        try:
            name = request.form['txtCategoryName'].lower()

            if category.verify_name(name):
                flash("Nombre de Categoría Existente", "warning")
                return redirect(url_for("admin_panel_categories"))
        except Exception as e:
            print(e)
            flash("Error Validar Nombre", "error")
            return redirect(url_for("admin_panel_categories"))

        # Revisar Referencial Unico
        try:
            referencial = request.form['txtCategoryReferencial'].lower()

            if category.verify_referencial(referencial):
                flash("Referencial de Categoría Existente", "warning")
                return redirect(url_for("admin_panel_categories"))
        except Exception as e:
            print(e)
            flash("Error Validar Referencial", "error")
            return redirect(url_for("admin_panel_categories"))

        # Añadir categoria
        try:
            db.session.add(category)
            db.session.commit()
            flash("Categoría Creada", "success")
            return redirect(url_for("admin_panel_categories"))

        except Exception as e:
            print(e)
            flash("Error Procesar Categoria", "error")
            return redirect(url_for("admin_panel_categories"))


@app.route("/admin-panel/categories/delete-category/<int:delete_id>", methods=["POST"])
def admin_panel_categories_delete_category(delete_id):
    if request.method == 'POST':
        if isinstance(delete_id, int):
            return redirect(url_for("admin_panel_categories_confirm_deletion", delete_id=delete_id))
        else:
            flash("Error de ID", "error")
            return redirect(url_for("admin_panel_categories"))

    flash("Error de Método", "error")
    return redirect(url_for("admin_panel_categories"))


@app.route("/admin-panel/products/add-product", methods=["POST", "GET"])
def admin_panel_products_add_product():
    if request.method == 'POST':
        product = Products(category_id=request.form['txtCategoryId'],
                           supplier_id=request.form['txtSupplierId'],
                           product_name=request.form['txtProductName'],
                           product_price=request.form['txtProductPrice'],
                           product_selling_price=request.form['txtProductSellingPrice'],
                           product_referencial=request.form['txtProductReferencial'],
                           product_limit_stock=request.form['txtProductLimitStock'],
                           product_active_stock=request.form['txtProductActiveStock'],
                           product_warehouse=request.form['txtProductWarehouse'],
                           product_zone=request.form['txtProductZone'],
                           product_description=request.form['txtProductDescription'])
    else:
        flash("Error de Método", "error")
        return redirect(url_for("admin_panel_categories"))

    # Revisar Referencial Unico
    try:
        referencial = request.form['txtProductReferencial'].lower()

        if product.verify_referencial(referencial):
            flash("Referencial de Producto Existente", "warning")
            return redirect(url_for("admin_panel_products"))
    except Exception as e:
        print(e)
        flash("Error Validar Referencial", "error")
        return redirect(url_for("admin_panel_products"))

    # Validar Categoria
    try:
        cateogry_id = request.form['txtCategoryId']

        if not product.verify_category(cateogry_id):
            flash("La Categoria No Existe", "warning")
            return redirect(url_for("admin_panel_products"))
    except Exception as e:
        print(e)
        flash("Error Validar Categoria", "error")
        return redirect(url_for("admin_panel_products"))

    # Validar Proveedor
    try:
        supplier_id = request.form['txtSupplierId']

        if not product.verify_supplier(supplier_id):
            flash("El Proveedor No Existe", "warning")
            return redirect(url_for("admin_panel_products"))
    except Exception as e:
        print(e)
        flash("Error Validar Proveedor", "error")
        return redirect(url_for("admin_panel_products"))

    # Validar Stock
    try:
        limit_stock = int(request.form['txtProductLimitStock'])
        product.product_limit_stock = product.verify_limit_stock(limit_stock)
    except Exception as e:
        print(e)
        flash("Error al validar Límite de Stock", "error")
        return redirect(url_for("admin_panel_products"))

    try:
        limit_stock = int(request.form['txtProductLimitStock'])
        active_stock = int(request.form['txtProductActiveStock'])
        product.product_active_stock = product.verify_active_stock(active_stock, limit_stock)
    except Exception as e:
        print(e)
        flash("Error al validar Stock Activo", "error")
        return redirect(url_for("admin_panel_products"))

    # Añadir producto
    try:
        db.session.add(product)
        db.session.commit()
        flash("Producto Creado", "success")
        return redirect(url_for("admin_panel_products"))

    except Exception as e:
        print(e)
        flash("Error Procesar Producto", "error")
        return redirect(url_for("admin_panel_products"))


@app.route("/admin-panel/products/delete-product/<int:delete_id>", methods=["POST", "GET"])
def admin_panel_products_delete_product(delete_id):
    if request.method == 'POST':
        if isinstance(delete_id, int):
            return redirect(url_for("admin_panel_products_confirm_deletion", delete_id=delete_id))
        else:
            flash("Error de ID", "error")
            return redirect(url_for("admin_panel_products"))
    else:
        flash("Error de Método", "error")
        return redirect(url_for("admin_panel_products"))

# Definimos un bucle if main para ejecutar la web
if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
    app.run(debug=True)
