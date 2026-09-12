import os

from dotenv import load_dotenv

load_dotenv()


def get_required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(f"{name} is not configured")

    return value

DEEPSEEK_API_KEY = get_required_env("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = get_required_env("DEEPSEEK_BASE_URL")
DEEPSEEK_MODEL = get_required_env("DEEPSEEK_MODEL")