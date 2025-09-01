# --- imports section --- #
# dotenv variables
from dotenv import load_dotenv
# General system libraries
from pathlib import Path
from os import getenv

def set_env_file(path: str = "/.env.hcs"):
    load_dotenv(Path(path))
    print(getenv('OLLAMA_URL'))

