import requests

API_URL = "https://api.telegram.org"


def build_report(profile, repos, emails):
    lines = [f"GitHub: {profile['login']}"]
    for key, title in [("name", "Имя"), ("company", "Компания"), ("location", "Город"), ("blog", "Сайт")]:
        if profile.get(key):
            lines.append(f"{title}: {profile[key]}")
    lines.append(f"Аккаунт создан: {profile['created_at'][:10]}")
    lines.append(f"Публичных репозиториев: {len(repos)}")
    lines.extend(f"  {name}" for name in repos[:10])
    if emails:
        lines.append("Почта из коммитов:")
        lines.extend(f"  {email}" for email in emails)
    else:
        lines.append("Почта из коммитов не найдена")
    return "\n".join(lines)


def send_message(text, token, chat_id, proxy=None):
    proxies = {"http": proxy, "https": proxy} if proxy else None
    response = requests.post(
        f"{API_URL}/bot{token}/sendMessage",
        json={"chat_id": chat_id, "text": text},
        proxies=proxies,
        timeout=10,
    )
    response.raise_for_status()
