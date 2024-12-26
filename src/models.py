import db
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class Users(db.Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(Integer, ForeignKey("roles.role_id"), nullable=False)
    user_email = Column(String(200), nullable=False)
    user_password = Column(String(200), nullable=False)


    def __init__(self, user_email, user_password, admin):
        self.user_email = user_email
        self.user_password = user_password
        self.admin = admin

    def __repr__(self):
        return "User {}: {} {} ({})".format(self.user_id, self.user_name, self.user_password, self.admin)

    def __str__(self):
        return "User {}: {} {} ({})".format(self.user_id, self.user_name, self.user_password, self.admin)

class Roles(db.Base):
    __tablename__ = "roles"
    role_id = Column(Integer, primary_key=True, autoincrement=False)
    role_name = Column(String(100), nullable=False)

    def __init__(self, role_id, role_name):
        self.role_id = role_id
        self.role_name = role_name

    def __repr__(self):
        return "Role {}: ID {}".format(self.role_name, self.role_id)

    def __str__(self):
        return "Role {}: ID {}".format(self.role_name, self.role_id)