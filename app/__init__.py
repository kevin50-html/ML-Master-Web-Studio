# app/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from config import Config   # 👈 importa la Config correcta

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(
        __name__,
        static_folder="static",
        template_folder=os.path.join(os.path.dirname(__file__), "..", "templates"),
    )

    # Cargar toda la config (SECRET_KEY y SQLALCHEMY_DATABASE_URI ya vienen de Config)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Ruta de salud para Render
    @app.get("/healthz")
    def healthz():
        return "ok", 200

    # ✅ Ruta de prueba de DB (temporal, solo para debug en Render)
    @app.get("/dbcheck")
    def dbcheck():
        try:
            with db.engine.connect() as conn:
                conn.exec_driver_sql("SELECT 1")
            return "db ok", 200
        except Exception as e:
            return f"db error: {e}", 500

    from app.controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.controllers.main_controller import main_controller
    app.register_blueprint(main_controller)

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))

    return app