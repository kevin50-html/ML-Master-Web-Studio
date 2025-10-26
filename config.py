# config.py
from urllib.parse import urlsplit, urlunsplit
from dotenv import load_dotenv
import os

load_dotenv()


def _force_psycopg(url: str | None) -> str | None:
    if not url:
        return url
    parts = urlsplit(url)

    # Si la URL empieza con "postgres://" o "postgresql://"
    if parts.scheme in ("postgres", "postgresql", "postgresql+psycopg2"):
        scheme = "postgresql+psycopg"
        url = urlunsplit((scheme, parts.netloc, parts.path, parts.query, parts.fragment))

    return url


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "mi_clave_secreta")

    # URL de Render (EXTERNAL CONNECTION)
    DATABASE_URL = os.environ.get("postgresql://mlmasterwebstudio_db_user:8fPVbhUQsvGsm7gw47ByWYjIL5vA00Zb@dpg-d3sf35q4d50c738q5nfg-a.oregon-postgres.render.com/mlmasterwebstudio_db")

    SQLALCHEMY_DATABASE_URI = _force_psycopg(DATABASE_URL)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
