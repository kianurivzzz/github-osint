import sys

import config
from github_api import get_commit_emails, get_profile, get_repos
from telegram_bot import build_report, send_message


def main():
    if len(sys.argv) != 2:
        print("Использование: python main.py <логин>")
        sys.exit(1)
    login = sys.argv[1]
    profile = get_profile(login, config.GITHUB_TOKEN)
    repos = get_repos(login, config.GITHUB_TOKEN)
    emails = get_commit_emails(login, repos, config.GITHUB_TOKEN)
    report = build_report(profile, repos, emails)
    send_message(report, config.TELEGRAM_BOT_TOKEN, config.TELEGRAM_CHAT_ID)
    print("Сводка отправлена")


if __name__ == "__main__":
    main()
