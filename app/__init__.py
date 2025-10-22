from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Inicialización de las extensiones
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(
        __name__,
        static_folder='static',
        template_folder=os.path.join(os.path.abspath(os.path.dirname(__file__)), '../templates')
    )

    # Configurar la base de datos y la clave secreta
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'mi_clave_secreta')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://usuario:contraseña@localhost:3306/base_de_datos')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar las extensiones
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Registrar el Blueprint para autenticación
    from app.controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Registrar el Blueprint para las rutas principales
    from app.controllers.main_controller import main_controller
    app.register_blueprint(main_controller)

    # Cargar el usuario para la sesión de login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))

    return app
