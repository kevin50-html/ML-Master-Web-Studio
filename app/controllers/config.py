from dotenv import load_dotenv
import os

load_dotenv()

def _normalize_database_url(url: str | None) -> str | None:
    if not url:
        return url
    # Render suele dar postgres://... ; SQLAlchemy espera postgresql+psycopg://...
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg://", 1)
    elif url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "mi_clave_secreta")
    # Fallback local (MySQL). En Render se usará DATABASE_URL.
    DEFAULT_LOCAL_URI = "mysql+pymysql://mlmasterwebstudio:#$fsd5sd7fd6637jhgD@localhost:3306/mlmasterwebstudio?charset=utf8mb4"

    SQLALCHEMY_DATABASE_URI = _normalize_database_url(
        os.environ.get("DATABASE_URL", DEFAULT_LOCAL_URI)
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
