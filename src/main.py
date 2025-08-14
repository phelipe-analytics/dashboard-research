import os, json, gzip, requests
from datetime import datetime
from bs4 import BeautifulSoup
from get_repo_details import get_repo_details

BASE_URL = "https://github.com/trending/{lang}?since=daily"
OUTPUT_DIR = "data"

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open("languages.json", "r", encoding="utf-8") as f:
    languages = json.load(f)

languages.insert(0, "All")  # Adiciona a opção sem linguagem

all_data = {}

def scrape_trending_for_language(lang: str):
    """Coleta os repositórios trending de uma linguagem específica."""
    print(f"🔍 Coletando repositórios de: {lang}", flush=True)
    
    url = BASE_URL.format(lang="" if lang == "All" else lang)
    response = requests.get(url)
    if response.status_code != 200:
        print(f"⚠ Erro ao acessar {lang}: {response.status_code}", flush=True)
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    repos_for_lang = []

    for repo in soup.find_all("article", class_="Box-row"):
        repo_name = repo.h2.a.get_text(strip=True).replace("\n", "").replace(" ", "")
        print(f"\t🔹 Coletando dados de {repo_name}...", flush=True) 
        
        stars_today_tag = repo.find("span", class_="d-inline-block float-sm-right")
        stars_today = stars_today_tag.get_text(strip=True).split()[0] if stars_today_tag else "0"

        details = get_repo_details(repo_name, info_type="details")
        contributors = get_repo_details(repo_name, info_type="contributors")
        pulls = get_repo_details(repo_name, info_type="pulls")
        branches = get_repo_details(repo_name, info_type="branches")

        if details:
            repo_data = {
                **details,
                "stars_today": stars_today,
                "language_scraped": lang,
                "top_contributors": contributors,
                "pull_requests": pulls,
                "branches": branches
            }
            repos_for_lang.append(repo_data)
            print(f"\t✅ Dados de {repo_name} coletados com sucesso!", flush=True) 

    print(f"✅ {len(repos_for_lang)} repositórios coletados para {lang}", flush=True)
    return repos_for_lang


for lang in languages:
    all_data[lang] = scrape_trending_for_language(lang)

today_str = datetime.now().strftime("%Y-%m-%d")
file_name = os.path.join(OUTPUT_DIR, f"{today_str}.json.gz")

with gzip.open(file_name, "wt", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)

print(f"🎉 Dados salvos em {file_name}", flush=True)
