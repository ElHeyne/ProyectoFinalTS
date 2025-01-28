import db
from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, DateTime, text
from werkzeug.security import generate_password_hash, check_password_hash


class Users(db.Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.role_id"), nullable=False)
    user_email = Column(String(255), nullable=False)
    user_hash_password = Column(String(255), nullable=False)
    user_name = Column(String(255), nullable=False, server_default="unidentified_user")
    user_register_date = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    def __init__(self, role_id, user_email, user_name):
        self.role_id = role_id
        self.user_email = user_email
        self.user_name = user_name

    def __repr__(self):
        return "User {}:{},{},{},{}".format(self.user_id, self.user_name, self.user_email, self.user_hash_password,
                                            self.role_id, self.user_register_date)

    def __str__(self):
        return "User {}:{},{},{},{}".format(self.user_id, self.user_name, self.user_email, self.user_hash_password,
                                            self.role_id, self.user_register_date)

    @property
    def user_password(self):
        raise AttributeError('Password is not a readable Attribute!')

    @user_password.setter
    def user_password(self, password):
        self.user_hash_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.user_hash_password, password)

    @staticmethod
    def verify_mail(mail):
        mail_check = db.session.query(Users).filter_by(user_email=mail).first()
        return mail_check is not None


class Roles(db.Base):
    __tablename__ = "roles"
    role_id = Column(Integer, primary_key=True, autoincrement=False)
    role_name = Column(String(255), nullable=False)

    def __init__(self, role_id, role_name):
        self.role_id = role_id
        self.role_name = role_name

    def __repr__(self):
        return "Role {}:{}".format(self.role_id, self.role_name)

    def __str__(self):
        return "Role {}:{}".format(self.role_id, self.role_name)


class Suppliers(db.Base):
    __tablename__ = "suppliers"
    supplier_id = Column(Integer, primary_key=True)
    supplier_name = Column(String(255), nullable=False, server_default="unidentified_supplier")
    supplier_phone = Column(Integer, nullable=False, server_default="0000")
    supplier_commercial_address = Column(String(255), nullable=False, server_default="unidentified_comercial_address")
    supplier_country = Column(String(255), nullable=False, server_default="unidentified_country")
    supplier_nif = Column(String(255), nullable=False, server_default="unidentified_nif")
    supplier_discount = Column(Integer, nullable=False, server_default="0")
    supplier_iva = Column(Integer, nullable=False, server_default="0")

    def __init__(self, supplier_name, supplier_phone, supplier_commercial_address, supplier_country, supplier_nif,
                 supplier_discount, supplier_iva):
        self.supplier_name = supplier_name
        self.supplier_phone = supplier_phone
        self.supplier_commercial_address = supplier_commercial_address
        self.supplier_country = supplier_country
        self.supplier_nif = supplier_nif
        self.supplier_discount = supplier_discount
        self.supplier_iva = supplier_iva

    def __repr__(self):
        return "Supplier {}:{},{},{},{},{},{},{}".format(self.supplier_id, self.supplier_name, self.supplier_phone,
                                                         self.supplier_commercial_address, self.supplier_country,
                                                         self.supplier_nif, self.supplier_discount, self.supplier_iva)

    def __str__(self):
        return "Supplier {}:{},{},{},{},{},{},{}".format(self.supplier_id, self.supplier_name, self.supplier_phone,
                                                         self.supplier_commercial_address, self.supplier_country,
                                                         self.supplier_nif, self.supplier_discount, self.supplier_iva)


class Categories(db.Base):
    __tablename__ = "categories"
    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(255), nullable=False, server_default="unidentified_category")
    category_referencial = Column(String(255), nullable=False, server_default="unidentified_referencial")
    category_zone = Column(String(255), nullable=True, server_default="unidentified_zone")

    def __init__(self, category_name, category_referencial, category_zone):
        self.category_name = category_name
        self.category_referencial = category_referencial
        self.category_zone = category_zone

    def __repr__(self):
        return "Category {}:{},{},{}".format(self.category_id, self.category_name, self.category_referencial,
                                             self.category_zone)

    def __str__(self):
        return "Category {}:{},{},{}".format(self.category_id, self.category_name, self.category_referencial,
                                             self.category_zone)


class Products(db.Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.supplier_id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=False)
    product_name = Column(String(255), nullable=False, server_default="unidentified_product")
    product_price = Column(DECIMAL(255, 2), nullable=False, server_default="0.00")
    product_referencial = Column(String(255), nullable=False, server_default="unidentified_referencial")
    product_limit_stock = Column(Integer, nullable=False, server_default="1")
    product_active_stock = Column(Integer, nullable=False, server_default="0")
    product_warehouse = Column(String(255), nullable=False,
                               server_default="unidentified_warehouse")  # Es una ubicacion como calle o codigo.
    product_zone = Column(String(255), nullable=False, server_default="unidentified_zone")

    def __init__(self, supplier_id, category_id, product_name, product_price, product_referencial, product_limit_stock,
                 product_active_stock, product_warehouse, product_zone):
        self.supplier_id = supplier_id
        self.category_id = category_id
        self.product_name = product_name
        self.product_price = product_price
        self.product_referencial = product_referencial
        self.product_limit_stock = product_limit_stock
        self.product_active_stock = product_active_stock
        self.product_warehouse = product_warehouse
        self.product_zone = product_zone

    def __repr__(self):
        return "Product {}:{},{},{},{},{},{},{},{},{}".format(self.product_id, self.supplier_id, self.category_id,
                                                              self.product_name, self.product_price,
                                                              self.product_referencial, self.product_limit_stock,
                                                              self.product_active_stock, self.product_warehouse,
                                                              self.product_zon)

    def __str__(self):
        return "Product {}:{},{},{},{},{},{},{},{},{}".format(self.product_id, self.supplier_id, self.category_id,
                                                              self.product_name, self.product_price,
                                                              self.product_referencial, self.product_limit_stock,
                                                              self.product_active_stock, self.product_warehouse,
                                                              self.product_zon)
