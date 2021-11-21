from pathlib import Path

from dotenv import load_dotenv


def load_flask_env() -> None:
    """Chargement du .env.flask situé dans le dossier si le .env.flask existe."""
    project_dir = Path(__file__).resolve().parent
    env_file = project_dir.joinpath('.env.flask')
    load_dotenv(env_file)


if __name__ == '__main__':
    load_flask_env()
