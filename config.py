import os
from dotenv import load_dotenv

load_dotenv()


def _get_config(key: str, default: str) -> str:
    """读取配置：优先 Streamlit Secrets（云端），其次 .env 环境变量（本地）"""
    try:
        import streamlit as st
        return st.secrets.get(key, os.getenv(key, default))
    except Exception:
        return os.getenv(key, default)


DEEPSEEK_API_KEY = _get_config("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = _get_config("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
DEEPSEEK_MODEL = _get_config("DEEPSEEK_MODEL", "deepseek-v4-pro")

PROVIDERS = {
    "deepseek": {
        "base_url": DEEPSEEK_BASE_URL,
        "api_key": DEEPSEEK_API_KEY,
        "model": DEEPSEEK_MODEL,
    },
    "openai": {
        "base_url": _get_config("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        "api_key": _get_config("OPENAI_API_KEY", ""),
        "model": _get_config("OPENAI_MODEL", "gpt-4o"),
    },
}

DEFAULT_PROVIDER = "deepseek"

MAX_RETRIES = 3
REQUEST_TIMEOUT = 60
