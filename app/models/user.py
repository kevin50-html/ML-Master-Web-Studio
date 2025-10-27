# app/models/user.py

from datetime import datetime
from flask_login import UserMixin
from app import bcrypt, db


class User(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    identification_type = db.Column(db.String(50), nullable=False)
    identification_number = db.Column(db.String(120), nullable=False)
    nationality = db.Column(db.String(120), nullable=False)
    sex = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    place_of_birth = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profession = db.Column(db.String(120), nullable=False)
    club = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

    # Establecer la contraseña hasheada antes de almacenarla
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Verificar la contraseña ingresada con el hash almacenado
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
