import os
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(PROJECT_DIR, 'streamer.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Dev(Config):
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True
