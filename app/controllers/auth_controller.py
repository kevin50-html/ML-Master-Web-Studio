# app/controllers/auth_controller.py

from datetime import datetime


from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError
from urllib.parse import urlparse, urljoin

from app import db
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

def _is_safe_url(target: str) -> bool:
    if not target:
        return False
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return (test_url.scheme in ('http', 'https')) and (ref_url.netloc == test_url.netloc)

# -------------------------
# Login
# -------------------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)  # puedes pasar remember=bool si tienes checkbox
            flash('¡Bienvenido!', 'success')

            next_page = request.args.get('next')
            if next_page and _is_safe_url(next_page):
                return redirect(next_page)
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Correo o contraseña incorrectos', 'danger')
            # No hacemos redirect para no perder el email
            return render_template('login.html', email=email)

    # GET
    return render_template('login.html')

# -------------------------
# Dashboard (protegido)
# -------------------------
@auth_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# -------------------------
# Logout
# -------------------------
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('auth.login_page'))

# -------------------------
# Registro Nuevos Usuarios
# -------------------------
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        date_of_birth_raw = request.form.get('date_of_birth', '').strip()
        identification_type = request.form.get('identification_type', '').strip()
        identification_number = request.form.get('identification_number', '').strip()
        nationality = request.form.get('nationality', '').strip()
        sex = request.form.get('sex', '').strip()
        gender = request.form.get('gender', '').strip()
        place_of_birth = request.form.get('place_of_birth', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip().lower()
        profession = request.form.get('profession', '').strip()
        club = request.form.get('club', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        required_fields = [
            first_name,
            last_name,
            date_of_birth_raw,
            identification_type,
            identification_number,
            nationality,
            sex,
            gender,
            place_of_birth,
            phone,
            email,
            profession,
            club,
            password,
            confirm_password,
        ]

        if not all(required_fields):
            flash('Todos los campos son obligatorios. Por favor, completa el formulario.', 'danger')
            return redirect(url_for('auth.register'))

        # Verificar si las contraseñas coinciden
        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'danger')
            return redirect(url_for('auth.register'))  # Redirigir al formulario de registro
            

        try:
            date_of_birth = datetime.strptime(date_of_birth_raw, '%Y-%m-%d').date()
        except ValueError:
            flash('La fecha de nacimiento no es válida. Usa el formato AAAA-MM-DD.', 'danger')
            return redirect(url_for('auth.register'))

        # Verificar si el usuario ya existe
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('El correo electrónico ya está registrado', 'danger')
        # Hashear la contraseña
            return redirect(url_for('auth.register'))

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            identification_type=identification_type,
            identification_number=identification_number,
            nationality=nationality,
            sex=sex,
            gender=gender,
            place_of_birth=place_of_birth,
            phone=phone,
            email=email,
            profession=profession,
            club=club,
        )
        new_user.set_password(password)

        # Crear el nuevo usuario
        db.session.add(new_user)
        db.session.commit()

        flash('Cuenta creada con éxito', 'success')
        return redirect(url_for('auth.login_page'))  # Redirigir al login después de crear la cuenta

    return render_template('register.html')  # Mostrar el formulario de registro