import db
from sqlalchemy import Column, Integer, String, Boolean

class Users(db.Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_email = Column(String(200), nullable=False)
    user_password = Column(String(200), nullable=False)
    admin = Column(Boolean)

    def __init__(self, user_email, user_password, admin):
        self.user_email = user_email
        self.user_password = user_password
        self.admin = admin

    def __repr__(self):
        return "User {}: {} {} ({})".format(self.user_id, self.user_name, self.user_password, self.admin)

    def __str__(self):
        return "User {}: {} {} ({})".format(self.user_id, self.user_name, self.user_password, self.admin)
