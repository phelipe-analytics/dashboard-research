# main.py
import json
import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from get_repo_details import get_repo_details

BASE_URL = "https://github.com/trending/{lang}?since=daily"
OUTPUT_DIR = "data"

# Garante que a pasta existe
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Lê as linguagens
with open("languages.json", "r", encoding="utf-8") as f:
    languages = json.load(f)

languages.insert(0, "All")  # Adiciona a opção sem linguagem

all_data = {}

for lang in languages:
    print(f"🔍 Coletando repositórios de: {lang}")
    url = BASE_URL.format(lang="" if lang == "All" else lang)
    response = requests.get(url)
    if response.status_code != 200:
        print(f"⚠ Erro ao acessar {lang}: {response.status_code}")
        all_data[lang] = []
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    repos_for_lang = []

    for repo in soup.find_all("article", class_="Box-row"):
        repo_name = repo.h2.a.get_text(strip=True).replace("\n", "").replace(" ", "")
        stars_today_tag = repo.find("span", class_="d-inline-block float-sm-right")
        stars_today = stars_today_tag.get_text(strip=True).split()[0] if stars_today_tag else "0"

        details = get_repo_details(repo_name)
        if details:
            repos_for_lang.append(details | {"stars_today": stars_today, "language_scraped": lang})

    all_data[lang] = repos_for_lang
    print(f"✅ {len(repos_for_lang)} repositórios coletados para {lang}")

# Salva o arquivo do dia
today_str = datetime.now().strftime("%Y-%m-%d")
file_name = os.path.join(OUTPUT_DIR, f"trending_repos_{today_str}.json")

with open(file_name, "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)

print(f"🎉 Dados salvos em {file_name}")
