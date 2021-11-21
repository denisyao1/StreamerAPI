"""
load_env_file module permettant de charger les variables d'environnement à partir d'un env file
si le .env file existe. Si une variable d'environnement est déjà définie, elle ne sera pas écrasée.
"""
from pathlib import Path

from dotenv import load_dotenv


def load_env() -> None:
    """Chargement du .env situé dans le dossier si le .env existe."""

    project_dir = Path(__file__).resolve().parent.parent
    env_file = project_dir.joinpath('.env')
    load_dotenv(env_file)


if __name__ == '__main__':
    load_env()
