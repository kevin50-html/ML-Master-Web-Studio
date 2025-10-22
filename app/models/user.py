# app/models/user.py
from app import db
from flask_login import UserMixin
from app import bcrypt

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

    # Establecer la contraseña hasheada antes de almacenarla
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Verificar la contraseña ingresada con el hash almacenado
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
