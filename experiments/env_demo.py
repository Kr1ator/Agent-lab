import os

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("LLM_API_KEY")

if api_key is None:
    raise RuntimeError("LLM_API_KEY is not configured")

print("Configuration loaded successfully.")