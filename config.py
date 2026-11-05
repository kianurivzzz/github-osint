import os

from dotenv import load_dotenv

load_dotenv()


def require(name):
    value = os.getenv(name)
    if not value:
        raise SystemExit(f"Не задана переменная {name}. Скопируй .env.example в .env и впиши значение")
    return value


GITHUB_TOKEN = require("GITHUB_TOKEN")
TELEGRAM_BOT_TOKEN = require("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = require("TELEGRAM_CHAT_ID")
PROXY_URL = os.getenv("PROXY_URL")
