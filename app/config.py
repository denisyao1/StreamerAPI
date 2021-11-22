import os
from pathlib import Path

# getting project root directory path
PROJECT_DIR = Path(__file__).resolve().parent.parent


class Config:
    """
    Base configuration class
    """
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + str(PROJECT_DIR.joinpath('streamer.db')))
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Development(Config):
    """
    Development configuration class
    """
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True
