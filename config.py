import os
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-v4-pro")

PROVIDERS = {
    "deepseek": {
        "base_url": DEEPSEEK_BASE_URL,
        "api_key": DEEPSEEK_API_KEY,
        "model": DEEPSEEK_MODEL,
    },
    "openai": {
        "base_url": os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        "api_key": os.getenv("OPENAI_API_KEY", ""),
        "model": os.getenv("OPENAI_MODEL", "gpt-4o"),
    },
}

DEFAULT_PROVIDER = "deepseek"

MAX_RETRIES = 3
REQUEST_TIMEOUT = 60
