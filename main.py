import os
import sys

from dotenv import load_dotenv

from github_api import get_commit_emails, get_profile, get_repos
from telegram_bot import build_report, send_message


def main():
    load_dotenv()
    if len(sys.argv) != 2:
        print("Использование: python main.py <логин>")
        sys.exit(1)
    login = sys.argv[1]
    token = os.environ["GITHUB_TOKEN"]
    profile = get_profile(login, token)
    repos = get_repos(login, token)
    emails = get_commit_emails(login, repos, token)
    report = build_report(profile, repos, emails)
    send_message(report, os.environ["TELEGRAM_BOT_TOKEN"], os.environ["TELEGRAM_CHAT_ID"])
    print("Сводка отправлена")


if __name__ == "__main__":
    main()
