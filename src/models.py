import db
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class Users(db.Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.role_id"), nullable=False)
    user_email = Column(String(255), nullable=False)
    user_password = Column(String(255), nullable=False)
    user_name = Column(String(255), nullable=False, default="unidentified_user")

    def __init__(self, role_id, user_email, user_password, user_name):
        self.role_id = role_id
        self.user_email = user_email
        self.user_password = user_password
        self.user_name = user_name

    def __repr__(self):
        return "User {}: {} {} {} {}".format(self.user_id, self.user_name, self.user_email, self.user_password,
                                             self.role_id)

    def __str__(self):
        return "User {}: {} {} {} {}".format(self.user_id, self.user_name, self.user_email, self.user_password,
                                             self.role_id)


class Roles(db.Base):
    __tablename__ = "roles"
    role_id = Column(Integer, primary_key=True, autoincrement=False)
    role_name = Column(String(255), nullable=False)

    def __init__(self, role_id, role_name):
        self.role_id = role_id
        self.role_name = role_name

    def __repr__(self):
        return "Role {}: ID {}".format(self.role_name, self.role_id)

    def __str__(self):
        return "Role {}: ID {}".format(self.role_name, self.role_id)


class Suppliers(db.Base):
    __tablename__ = "suppliers"
    supplier_id = Column(Integer, primary_key=True)
    supplier_name = Column(String(255), nullable=False, default="unidentified_supplier")
    supplier_phone = Column(Integer, nullable=False, default=0000)
    supplier_commercial_address = Column(String(255), nullable=False, default="unidentified_comercial_address")
    supplier_country = Column(String(255), nullable=False, default="unidentified_country")
    supplier_nif = Column(String(255), nullable=False, default="unidentified_nif")
    supplier_discount = Column(Integer, nullable=False, default=0)
    supplier_iva = Column(Integer, nullable=False, default=0)

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
        return "Supplier {}: {} {} {} {} {} {} {}".format(self.supplier_name, self.supplier_id, self.supplier_phone,
                                                          self.supplier_commercial_address, self.supplier_country,
                                                          self.supplier_nif, self.supplier_discount, self.supplier_iva)

    def __str__(self):
        return "Supplier {}: {} {} {} {} {} {} {}".format(self.supplier_name, self.supplier_id, self.supplier_phone,
                                                          self.supplier_commercial_address, self.supplier_country,
                                                          self.supplier_nif, self.supplier_discount, self.supplier_iva)


class Categories(db.Base):
    __tablename__ = "categories"
    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(255), nullable=False, default="unidentified_category")
    category_referencial = Column(String(255), nullable=False, default="unidentified_referencial")
    category_zone = Column(String(255), nullable=True, defualt="unidentified_zone")

    def __init__(self, category_name, category_referencial, category_zone):
        self.category_name = category_name
        self.category_referencial = category_referencial
        self.category_zone = category_zone

    def __repr__(self):
        return "Category {}: {} {} {}".format(self.category_name, self.category_id, self.category_referencial,
                                              self.category_zone)

    def __str__(self):
        return "Category {}: {} {} {}".format(self.category_name, self.category_id, self.category_referencial,
                                              self.category_zone)


class Products(db.Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.supplier_id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.category_id"))