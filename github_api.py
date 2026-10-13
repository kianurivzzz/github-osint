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


def get_repos(login, token):
    data = _get(f"/users/{login}/repos", token, params={"per_page": 100, "sort": "updated"})
    return [repo["name"] for repo in data if not repo["fork"]]


def get_commit_emails(login, repos, token):
    emails = set()
    for repo in repos:
        try:
            commits = _get(f"/repos/{login}/{repo}/commits", token, params={"author": login, "per_page": 30})
        except requests.HTTPError:
            continue
        for commit in commits:
            email = commit["commit"]["author"]["email"]
            if not email.endswith("@users.noreply.github.com"):
                emails.add(email)
    return sorted(emails)
