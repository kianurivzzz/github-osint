import requests

API_URL = "https://api.github.com"


def _get(path, token, params=None):
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    response = requests.get(f"{API_URL}{path}", headers=headers, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def get_profile(login, token):
    data = _get(f"/users/{login}", token)
    return {
        "login": data["login"],
        "name": data.get("name"),
        "company": data.get("company"),
        "location": data.get("location"),
        "blog": data.get("blog"),
        "created_at": data["created_at"],
    }
