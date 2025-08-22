import os, json, gzip, requests
from datetime import datetime
from bs4 import BeautifulSoup
from collections import defaultdict
from get_repo_details import get_repo_details

BASE_URL = "https://github.com/trending/{lang}?since=daily"
OUTPUT_DIR = "data"

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open("languages.json", "r", encoding="utf-8") as f:
    languages = json.load(f)
    
with open("repos_collected.json", "r", encoding="utf-8") as f:
    repos_collected = json.load(f)

languages.insert(0, "trending")  

all_data = {}
trending_repos = []

# def scrape_trending_for_language(trending_lang: str):
#     """Coleta os repositórios trending de uma linguagem específica."""
#     print(f"🔍 Coletando repositórios de: {trending_lang}", flush=True)

#     url = BASE_URL.format(lang="" if trending_lang == "trending" else trending_lang)
#     response = requests.get(url)
#     if response.status_code != 200:
#         print(f"⚠ Erro ao acessar {trending_lang}: {response.status_code}", flush=True)
#         return []

#     soup = BeautifulSoup(response.text, "html.parser")
#     repos_for_lang = []

#     for repo in soup.find_all("article", class_="Box-row"):
#         repo_name = repo.h2.a.get_text(strip=True).replace("\n", "").replace(" ", "")
#         trending_repos.append(repo_name)
#         print(f"\t🔹 Coletando dados de {repo_name}...", flush=True) 
        
#         stars_today_tag = repo.find("span", class_="d-inline-block float-sm-right")
#         stars_today = stars_today_tag.get_text(strip=True).split()[0] if stars_today_tag else "0"

#         details = get_repo_details(repo_name, info_type="details")
#         contributors = get_repo_details(repo_name, info_type="contributors")
#         pulls = get_repo_details(repo_name, info_type="pulls")
#         branches = get_repo_details(repo_name, info_type="branches")

#         if details:
#             repo_data = {
#                 **details,
#                 "stars_today": stars_today,
#                 "top_contributors": contributors,
#                 "pull_requests": pulls,
#                 "branches": branches,
#                 "is_trending": trending_lang == "trending"
#             }
#             repos_for_lang.append(repo_data)
#             print(f"\t✅ Dados de {repo_name} coletados com sucesso!", flush=True) 

#     print(f"✅ {len(repos_for_lang)} repositórios coletados para {trending_lang}", flush=True)
#     return repos_for_lang
def get_trending_repos_name(trending_lang: str):
    url = BASE_URL.format(lang="" if trending_lang == "trending" else trending_lang)
    response = requests.get(url)
    if response.status_code != 200:
        print(f"⚠ Erro ao acessar {trending_lang}: {response.status_code}", flush=True)
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    for repo in soup.find_all("article", class_="Box-row"):
        repo_name = repo.h2.a.get_text(strip=True).replace("\n", "").replace(" ", "")
        trending_repos.append((repo_name, trending_lang == "trending"))

def fetch_repo_data(repo_name: str, is_trending: bool, all_stars_yesterday: int = 0):
    print(f"\t🔍 Coletando detalhes de: {repo_name}", flush=True)
    details = get_repo_details(repo_name, info_type="details")
    contributors = get_repo_details(repo_name, info_type="contributors")
    pulls = get_repo_details(repo_name, info_type="pulls")
    branches = get_repo_details(repo_name, info_type="branches")
    
    all_stars_today = details['stargazers_count']
    new_repos_collected[repo_name] = all_stars_today
    
    repo_data = {
        **details,
        "stars_today": all_stars_today - all_stars_yesterday,
        "top_contributors": contributors,
        "pull_requests": pulls,
        "branches": branches,
        "is_trending": is_trending
    }
    print(f"\t\t✅ Dados de {repo_name} coletados com sucesso!", flush=True)
    return repo_data
    

new_repos_collected = defaultdict(int)
repos = []
for lang in languages:
    get_trending_repos_name(lang)

for name, is_trending in trending_repos:
    if name not in [repo["name"] for repo in repos_collected]:
        repos.append(fetch_repo_data(name, is_trending))
    else:
        idx = [repo["name"] for repo in repos_collected].index(name)
        repos.append(fetch_repo_data(name, is_trending, repos_collected[idx]["stars"]))

for r in repos_collected:
    if r["name"] not in [repo[0] for repo in trending_repos]:
        repos.append(fetch_repo_data(r["name"], False, r["stars"]))


today_str = datetime.now().strftime("%Y-%m-%d")
file_name = os.path.join(OUTPUT_DIR, f"{today_str}.json.gz")

new_repos_collected_file_name = [{"name": name, "stars": stars} for name, stars in new_repos_collected.items()]
with open("repos_collected.json", "w", encoding="utf-8") as f:
    json.dump(new_repos_collected_file_name, f, indent=2, ensure_ascii=False)

with gzip.open(file_name, "wt", encoding="utf-8") as f:
    json.dump(repos, f, ensure_ascii=False, indent=2)

print(f"🎉 Dados salvos em {file_name}", flush=True)
