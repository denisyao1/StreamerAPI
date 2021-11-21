from pathlib import Path

from dotenv import load_dotenv


def load_env() -> None:
    """Loading of the .env located in the root folder if the .env exists."""

    project_dir = Path(__file__).resolve().parent.parent
    env_file = project_dir.joinpath('.env')
    load_dotenv(env_file)


if __name__ == '__main__':
    load_env()
