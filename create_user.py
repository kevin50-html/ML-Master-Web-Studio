from app import create_app, db, bcrypt
from app.models.user import User  # Importar correctamente el modelo User

# Crear la aplicación
app = create_app()

# Crear el usuario dentro del contexto de la app
with app.app_context():
    # Definir los datos del nuevo usuario
    email = 'demo@demo.com'
    password = 'Demo1234'

    # Generar el hash de la contraseña
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    # Crear el objeto de usuario
    user = User(email=email, password=password_hash)

    # Agregar el usuario a la base de datos
    db.session.add(user)
    db.session.commit()

    print('Usuario creado exitosamente.')
