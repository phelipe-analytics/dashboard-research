import os
import requests

TOKEN = os.getenv("GH_PAT")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

def get_repo_details(repo_name):
    url = f"https://api.github.com/repos/{repo_name}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        print(f"⚠ Erro ao acessar {repo_name}: {r.status_code}")
        return None

    return r.json()
