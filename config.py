import os
from pathlib import Path

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or os.urandom(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///contacts.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
