# auth_controller.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, current_user, logout_user  # Asegúrate de importar logout_user
from app import db, bcrypt
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

# Página de login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Buscar al usuario por email
        user = User.query.filter_by(email=email).first()

        # Verificar si el usuario existe y si la contraseña es correcta
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)  # Iniciar sesión
            flash('Bienvenido!', 'success')  # Mensaje de éxito
            return redirect(url_for('auth.dashboard'))  # Redirigir al dashboard
        else:
            flash('Correo o contraseña incorrectos', 'danger')  # Mensaje de error

    return render_template('login.html')  # Renderiza el formulario de login

# Ruta del Dashboard (solo para usuarios autenticados)
@auth_bp.route('/dashboard')
@login_required  # Ruta protegida para usuarios autenticados
def dashboard():
    return render_template('dashboard.html')  # Vista del dashboard

# Ruta de Logout
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()  # Cerrar sesión
    flash('Has cerrado sesión', 'info')  # Mensaje de info
    return redirect(url_for('auth.login_page'))  # Redirigir al login


#________________________________________________

# Página de registro de nuevos usuarios
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Verificar si las contraseñas coinciden
        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'danger')
            return redirect(url_for('auth.register'))  # Redirigir al formulario de registro

        # Verificar si el usuario ya existe
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('El correo electrónico ya está registrado', 'danger')
            return redirect(url_for('auth.register'))  # Redirigir al formulario de registro

        # Hashear la contraseña
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Crear el nuevo usuario
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Cuenta creada con éxito', 'success')
        return redirect(url_for('auth.login_page'))  # Redirigir al login después de crear la cuenta

    return render_template('register.html')  # Mostrar el formulario de registro