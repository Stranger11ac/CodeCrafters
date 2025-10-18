from dotenv import load_dotenv, set_key
from pathlib import Path
import secrets
import os

env_path = Path('.') / '.env'

if not env_path.exists():
    env_path.write_text("")

load_dotenv(dotenv_path=env_path)

if not os.getenv("SECRET_KEY"):
    new_key = secrets.token_urlsafe(48)
    from dotenv import set_key
    set_key(str(env_path), "SECRET_KEY", new_key)
    print("Se generó y guardó SECRET_KEY en .env")
else:
    print("SECRET_KEY ya existe en el entorno.")
