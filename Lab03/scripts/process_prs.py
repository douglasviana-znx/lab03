import requests
import csv

# Seu token do GitHub (IMPORTANTE ter para evitar bloqueios)
GITHUB_TOKEN = "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"  # coloque seu token aqui, ou deixe como None

def buscar_repositorios(top_n=200):
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"

    repositorios = []
    page = 1

    while len(repositorios) < top_n:
        url = f"https://api.github.com/search/repositories?q=stars:>1000&sort=stars&order=desc&per_page=100&page={page}"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"⚠️ Erro {response.status_code} ao buscar repositórios.")
            break

        data = response.json()
        items = data.get('items', [])
        for item in items:
            repositorios.append(item['full_name'])
            if len(repositorios) >= top_n:
                break

        page += 1

    print(f"✅ Total de repositórios encontrados: {len(repositorios)}")
    return repositorios

def coletar_prs(owner_repo):
    base_url = f"https://api.github.com/repos/{owner_repo}/pulls"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    
    prs = []
    page = 1

    while True:
        response = requests.get(base_url, headers=headers, params={"state": "all", "per_page": 100, "page": page})

        if response.status_code == 403:
            print(f"⚠️ Erro 403 ao coletar PRs de {owner_repo}. Pulando...")
            break
        elif response.status_code != 200:
            print(f"⚠️ Erro {response.status_code} ao coletar PRs de {owner_repo}. Pulando...")
            break
        
        data = response.json()
        if not data:
            break
        
        for pr in data:
            prs.append({
                "repo": owner_repo,
                "id": pr.get("id"),
                "number": pr.get("number"),
                "title": pr.get("title"),
                "user": pr.get("user", {}).get("login"),
                "state": pr.get("state"),
                "created_at": pr.get("created_at"),
                "closed_at": pr.get("closed_at"),
                "merged_at": pr.get("merged_at")
            })

        page += 1

    print(f"✅ Total de PRs coletados de {owner_repo}: {len(prs)}")
    return prs

def salvar_csv(prs, filename="data/processed/prs_dataset.csv"):
    if not prs:
        print("Nenhum PR para salvar no CSV.")
        return

    keys = prs[0].keys()
    with open(filename, mode="w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(prs)
    print(f"📄 Arquivo {filename} salvo com sucesso.")

def salvar_md(prs, filename="report/draft_report.md"):
    if not prs:
        print("Nenhum PR para salvar no Markdown.")
        return

    with open(filename, mode="w", encoding="utf-8") as f:
        f.write("# Pull Requests Coletados\n\n")
        for pr in prs:
            f.write(f"- **[{pr['repo']}] PR #{pr['number']}**: {pr['title']} (por {pr['user']})\n")
    print(f"📄 Arquivo {filename} salvo com sucesso.")

def main():
    repositorios = buscar_repositorios(200)  # agora buscando automaticamente
    all_prs = []

    for repo in repositorios:
        prs = coletar_prs(repo)
        all_prs.extend(prs)

    salvar_csv(all_prs)
    salvar_md(all_prs)

if __name__ == "__main__":
    main()
