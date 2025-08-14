import os
import requests
from typing import Literal

TOKEN = os.getenv("GH_PAT")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

def get_repo_details(repo_name, info_type: Literal["details", "branches", "contributors", "pulls"] = 'details'):
    suffix = "" if info_type == 'details' else f"/{info_type}?per_page=100"
    url = f"https://api.github.com/repos/{repo_name}{suffix}"
    print(f"\t🔹 Coletando {info_type} de {repo_name}...", flush=True) 

    r = requests.get(url, headers=HEADERS)
    
    # Define descrição legível do tipo de dado
    type_desc = "detalhes" if info_type == 'details' else info_type

    if r.status_code == 401:
        print(f"⚠ Erro de autenticação ao acessar {repo_name} ({type_desc})", flush=True)
        return None
    elif r.status_code != 200:
        print(f"⚠ Erro ao acessar {repo_name}: {r.status_code} ({type_desc})", flush=True)
        return None

    data = r.json()
    if isinstance(data, list):
        print(f"\t\t✅ {len(data)} itens coletados de {repo_name} ({type_desc})", flush=True) 
    else:
        print(f"\t\t✅ detalhes coletados de {repo_name}", flush=True)  
    
    return data
