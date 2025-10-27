from datetime import date

from app import create_app, db
from app.models.user import User  # Importar correctamente el modelo User

# Crear la aplicación
app = create_app()

# Crear el usuario dentro del contexto de la app
with app.app_context():
    # Definir los datos del nuevo usuario
    email = 'demo@demo.com'
    password = 'Demo1234'

    user = User(
        first_name='Usuario',
        last_name='Demostración',
        date_of_birth=date(1990, 1, 1),
        identification_type='Cédula de ciudadanía',
        identification_number='1234567890',
        nationality='Colombiana',
        sex='Masculino',
        gender='Masculino',
        place_of_birth='Bogotá',
        phone='+57 3000000000',
        email=email,
        profession='Ingeniero de software',
        club='Tecnología',
    )
    user.set_password(password)
    user.set_password(password)

    # Agregar el usuario a la base de datos
    db.session.add(user)
    db.session.commit()

    print('Usuario creado exitosamente.')
