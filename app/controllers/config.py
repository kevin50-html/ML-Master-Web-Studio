# config.py
from urllib.parse import urlsplit, urlunsplit
from dotenv import load_dotenv
import os

load_dotenv()

def _force_psycopg(url: str | None) -> str | None:
    if not url:
        return url
    parts = urlsplit(url)
    # "postgres://" o "postgresql://" o incluso "postgresql+psycopg2://"
    if parts.scheme in ("postgres", "postgresql", "postgresql+psycopg2"):
        scheme = "postgresql+psycopg"
        url = urlunsplit((scheme, parts.netloc, parts.path, parts.query, parts.fragment))
    return url

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "mi_clave_secreta")
    DEFAULT_LOCAL_URI = "mysql+pymysql://mlmasterwebstudio:#$fsd5sd7fd6637jhgD@localhost:3306/mlmasterwebstudio?charset=utf8mb4"
    SQLALCHEMY_DATABASE_URI = _force_psycopg(os.environ.get("DATABASE_URL", DEFAULT_LOCAL_URI))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
