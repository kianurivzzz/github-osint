import sys

import config
from github_api import get_commit_emails, get_profile, get_repos
from telegram_bot import build_report, send_message


def main():
    if len(sys.argv) != 2:
        print("Использование: python main.py <логин>")
        sys.exit(1)
    login = sys.argv[1]
    token = config.GITHUB_TOKEN
    proxy = config.PROXY_URL
    profile = get_profile(login, token, proxy)
    repos = get_repos(login, token, proxy)
    emails = get_commit_emails(login, repos, token, proxy)
    report = build_report(profile, repos, emails)
    send_message(report, config.TELEGRAM_BOT_TOKEN, config.TELEGRAM_CHAT_ID, proxy)
    print("Сводка отправлена")


if __name__ == "__main__":
    main()
