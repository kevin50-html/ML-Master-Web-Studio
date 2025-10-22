from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mi_clave_secreta')  # Usa la variable de entorno o un valor por defecto
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://mlmasterwebstudio:#$fsd5sd7fd6637jhgD@localhost:3306/mlmasterwebstudio?charset=utf8mb4'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
