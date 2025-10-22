from app import create_app, db, bcrypt
from app.models.user import User

# Crear la instancia de la aplicación Flask usando la función create_app
app = create_app()

# Crear un usuario de prueba si no existe (esto solo se ejecuta una vez)
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

# Este bloque solo se ejecuta cuando corres la aplicación de forma local
if __name__ == "__main__":
    app.run(debug=True)
