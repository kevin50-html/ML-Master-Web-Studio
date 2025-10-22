# run.py
from app import create_app, db, bcrypt
from app.models.user import User
from flask import Flask
from app.controllers.main_controller import main_controller  # Importa tu blueprint
app = Flask(__name__)
# Registrar el blueprint
app.register_blueprint(main_controller, url_prefix='/auth')  # Asegúrate de que tenga el prefijo correcto

app = create_app()

with app.app_context():
    email = 'demo@demo.com'
    password = 'Demo1234'

    # Verificar si el usuario ya existe
    existing_user = User.query.filter_by(email=email).first()
    
    if existing_user:
        print(f"El usuario con el correo {email} ya existe.")
    else:
        # Generar el hash de la contraseña
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Crear el objeto de usuario
        user = User(email=email, password=hashed_password)

        # Agregar el usuario a la base de datos
        db.session.add(user)
        db.session.commit()

        print(f"Usuario {email} creado exitosamente.")

if __name__ == "__main__":
    app.run(debug=True)
