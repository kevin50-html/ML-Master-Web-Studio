from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

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

    # Configuración de la base de datos y secret key
    app.config['SECRET_KEY'] = 'tu_clave_secreta'  # Cambia esto por una clave más segura
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mlmasterwebstudio:#$fsd5sd7fd6637jhgD@localhost:3306/mlmasterwebstudio?charset=utf8mb4'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar las extensiones
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Ruta para el login
    from app.controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Ruta para la página principal (si la tienes)
    from app.controllers.main_controller import main_controller
    app.register_blueprint(main_controller)

    # Cargar el usuario para la sesión de login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))


    return app
