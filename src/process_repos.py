import json
import os
from save_to_sqlite import save_to_sqlite

languages = [
    "python", "javascript", "typescript", "java", "go",
    "c", "c++", "csharp", "php", "ruby", "rust", "kotlin", "swift"
]

def normalize_repo(repo):
    return {
        "id": repo.get("id"),
        "name": repo.get("name"),
        "full_name": repo.get("full_name"),
        "html_url": repo.get("html_url"),
        "description": repo.get("description"),
        "language": repo.get("language"),
        "stargazers_count": repo.get("stargazers_count"),
        "stars_today": repo.get("stars_today"),
        "forks_count": repo.get("forks_count"),
        "watchers_count": repo.get("subscribers_count"),
        "open_issues_count": repo.get("open_issues_count"),
        "license": repo.get("license")["name"] if repo.get("license") else None,
        "topics": repo.get("topics", []),
        "default_branch": repo.get("default_branch"),
        "created_at": repo.get("created_at"),
        "updated_at": repo.get("updated_at"),
        "pushed_at": repo.get("pushed_at"),
        "owner": {
            "login": repo.get("owner", {}).get("login"),
            "id": repo.get("owner", {}).get("id"),
            "html_url": repo.get("owner", {}).get("html_url"),
            "type": repo.get("owner", {}).get("type")
        },
        "contributors": [
            {
                "login": c.get("login"),
                "id": c.get("id"),
                "contributions": c.get("contributions"),
                "html_url": c.get("html_url")
            } for c in repo.get("top_contributors") or []
        ],
        "pull_requests": [
            {
                "id": pr.get("id"),
                "number": pr.get("number"),
                "title": pr.get("title"),
                "state": pr.get("state"),
                "html_url": pr.get("html_url"),
                "created_at": pr.get("created_at"),
                "updated_at": pr.get("updated_at"),
                "merged_at": pr.get("merged_at")
            } for pr in repo.get("pull_requests", [])
        ],
        "branches": [
            {
                "name": b.get("name"),
                "sha": b.get("commit", {}).get("sha"),
                "url": b.get("commit", {}).get("url")
            } for b in repo.get("branches", [])
        ]
    }

def process_data(raw_data):
    """Processa dados mantendo a estrutura original."""
    processed = {}

    # All
    processed["All"] = [normalize_repo(r) for r in raw_data.get("All", [])]

    # Por linguagem
    for lang in languages:
        processed[lang] = [normalize_repo(r) for r in raw_data.get(lang, [])]

    return processed

def execute(file_path: str, file_name: str):
    # Lê JSON original
    with open(file_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    # Processa mantendo a estrutura original
    processed_data = process_data(raw_data)

    # Cria pasta para salvar JSON processado
    os.makedirs("data_processed", exist_ok=True)
    with open(f"data_processed/{file_name}", "w", encoding="utf-8") as f:
        json.dump(processed_data, f, indent=2)

    # Salva no banco de dados
    # Passamos a data da coleta (nome do arquivo sem extensão)
    collected_at = file_name.split(".")[0]
    save_to_sqlite('database.db', processed_data, collected_at=collected_at)
