import sqlite3
from datetime import datetime

def save_to_sqlite(db_path: str, data: dict, collected_at: str = None):
    if collected_at is None:
        collected_at = datetime.now().strftime("%Y-%m-%d")

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Repositórios
    c.execute("""
    CREATE TABLE IF NOT EXISTS repositories (
        id INTEGER,
        name TEXT,
        full_name TEXT,
        html_url TEXT,
        description TEXT,
        language TEXT,
        stargazers_count INTEGER,
        stars_today INTEGER,
        forks_count INTEGER,
        watchers_count INTEGER,
        open_issues_count INTEGER,
        license TEXT,
        topics TEXT,
        default_branch TEXT,
        created_at TEXT,
        updated_at TEXT,
        pushed_at TEXT,
        owner_login TEXT,
        owner_id INTEGER,
        owner_html_url TEXT,
        owner_type TEXT,
        collected_at TEXT,
        PRIMARY KEY (id, collected_at)
    )
    """)

    # Contributors
    c.execute("""
    CREATE TABLE IF NOT EXISTS contributors (
        repo_id INTEGER,
        login TEXT,
        id INTEGER,
        contributions INTEGER,
        html_url TEXT,
        collected_at TEXT,
        UNIQUE(repo_id, id, collected_at)
    )
    """)

    # Pull Requests
    c.execute("""
    CREATE TABLE IF NOT EXISTS pull_requests (
        repo_id INTEGER,
        id INTEGER,
        number INTEGER,
        title TEXT,
        state TEXT,
        html_url TEXT,
        created_at TEXT,
        updated_at TEXT,
        merged_at TEXT,
        collected_at TEXT,
        UNIQUE(repo_id, id, collected_at)
    )
    """)

    # Branches
    c.execute("""
    CREATE TABLE IF NOT EXISTS branches (
        repo_id INTEGER,
        name TEXT,
        sha TEXT,
        url TEXT,
        collected_at TEXT,
        UNIQUE(repo_id, name, collected_at)
    )
    """)

    # Inserir dados
    for repo in data.get("All", []) + [r for lang in data if lang != "All" for r in data[lang]]:
        # Repositórios
        c.execute("""
        INSERT OR REPLACE INTO repositories VALUES (
            :id, :name, :full_name, :html_url, :description, :language, :stargazers_count, :stars_today,
            :forks_count, :watchers_count, :open_issues_count, :license, :topics,
            :default_branch, :created_at, :updated_at, :pushed_at,
            :owner_login, :owner_id, :owner_html_url, :owner_type, :collected_at
        )
        """, {
            "id": repo.get("id"),
            "name": repo.get("name"),
            "full_name": repo.get("full_name"),
            "html_url": repo.get("html_url"),
            "description": repo.get("description"),
            "language": repo.get("language"),
            "stargazers_count": repo.get("stargazers_count"),
            "stars_today": repo.get("stars_today"),
            "forks_count": repo.get("forks_count"),
            "watchers_count": repo.get("watchers_count"),
            "open_issues_count": repo.get("open_issues_count"),
            "license": repo.get("license"),
            "topics": ",".join(repo.get("topics", [])),
            "default_branch": repo.get("default_branch"),
            "created_at": repo.get("created_at"),
            "updated_at": repo.get("updated_at"),
            "pushed_at": repo.get("pushed_at"),
            "owner_login": repo.get("owner", {}).get("login"),
            "owner_id": repo.get("owner", {}).get("id"),
            "owner_html_url": repo.get("owner", {}).get("html_url"),
            "owner_type": repo.get("owner", {}).get("type"),
            "collected_at": collected_at
        })

        # Contributors
        for contributor in repo.get("contributors", []):
            c.execute("""
            INSERT OR IGNORE INTO contributors VALUES (
                :repo_id, :login, :id, :contributions, :html_url, :collected_at
            )
            """, {
                "repo_id": repo.get("id"),
                "login": contributor.get("login"),
                "id": contributor.get("id"),
                "contributions": contributor.get("contributions"),
                "html_url": contributor.get("html_url"),
                "collected_at": collected_at
            })

        # Pull Requests
        for pr in repo.get("pull_requests", []):
            c.execute("""
            INSERT OR IGNORE INTO pull_requests VALUES (
                :repo_id, :id, :number, :title, :state, :html_url,
                :created_at, :updated_at, :merged_at, :collected_at
            )
            """, {
                "repo_id": repo.get("id"),
                "id": pr.get("id"),
                "number": pr.get("number"),
                "title": pr.get("title"),
                "state": pr.get("state"),
                "html_url": pr.get("html_url"),
                "created_at": pr.get("created_at"),
                "updated_at": pr.get("updated_at"),
                "merged_at": pr.get("merged_at"),
                "collected_at": collected_at
            })

        # Branches
        for branch in repo.get("branches", []):
            c.execute("""
            INSERT OR IGNORE INTO branches VALUES (
                :repo_id, :name, :sha, :url, :collected_at
            )
            """, {
                "repo_id": repo.get("id"),
                "name": branch.get("name"),
                "sha": branch.get("sha"),
                "url": branch.get("url"),
                "collected_at": collected_at
            })

    conn.commit()
    conn.close()
    print(f"Dados salvos no banco {db_path} com sucesso para a coleta {collected_at}!")
