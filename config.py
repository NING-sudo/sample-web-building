# config.py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / "instance"
INSTANCE_DIR.mkdir(exist_ok=True)

class Config:
    SECRET_KEY = "super-secret-key-change-in-prod"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{INSTANCE_DIR.as_posix()}/app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Simple auth
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "admin123"