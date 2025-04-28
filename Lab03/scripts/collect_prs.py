import os
import requests
import json
import time

# Caminhos para os arquivos e pastas
REPO_LIST_PATH = os.path.join("repos", "selected_repositories.txt")
RAW_DATA_PATH = os.path.join("data", "raw")

# Token do GitHub (obtido da variável de ambiente)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", None)

def get_prs(owner_repo, state="all", per_page=100, max_retries=3):
    """
    Coleta os Pull Requests de um repositório via GitHub API.
    Em caso de erro de conexão, tenta novamente até max_retries vezes.
    """
    base_url = f"https://api.github.com/repos/{owner_repo}/pulls"
    headers = {"Accept": "application/vnd.github.v3+json"}
    GITHUB_TOKEN = "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"
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    
    all_prs = []
    page = 1

    while True:
        params = {"state": state, "per_page": per_page, "page": page}
        retry_count = 0

        while retry_count < max_retries:
            try:
                response = requests.get(base_url, headers=headers, params=params, timeout=10)
                break  # Se a requisição for bem-sucedida, sai do loop de retry.
            except requests.exceptions.RequestException as e:
                retry_count += 1
                print(f"Erro ao coletar PRs de {owner_repo} na página {page}: {e}. Tentando novamente ({retry_count}/{max_retries})...")
                time.sleep(5)  # Aguarda 5 segundos antes de tentar novamente.

        if retry_count == max_retries:
            print(f"Falha ao coletar PRs de {owner_repo} após {max_retries} tentativas.")
            break

        if response.status_code != 200:
            print(f"Erro {response.status_code} ao coletar PRs de {owner_repo}.")
            break

        prs_page = response.json()
        if not prs_page:
            break

        all_prs.extend(prs_page)
        page += 1

    return all_prs

def save_prs_to_json(owner_repo, prs_data):
    """
    Salva os dados coletados dos PRs em um arquivo JSON dentro da pasta RAW_DATA_PATH.
    """
    file_name = owner_repo.replace("/", "_") + "_prs.json"
    output_path = os.path.join(RAW_DATA_PATH, file_name)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(prs_data, f, indent=2, ensure_ascii=False)

def main():
    # Cria a pasta para os dados brutos, se não existir
    os.makedirs(RAW_DATA_PATH, exist_ok=True)
    
    if not os.path.exists(REPO_LIST_PATH):
        print(f"Arquivo {REPO_LIST_PATH} não encontrado.")
        return

    with open(REPO_LIST_PATH, "r", encoding="utf-8") as repo_file:
        for line in repo_file:
            repo = line.strip()
            if not repo or repo.startswith("#"):
                continue

            # Define o caminho do arquivo JSON de saída para o repositório
            output_file = repo.replace("/", "_") + "_prs.json"
            output_path = os.path.join(RAW_DATA_PATH, output_file)
            
            # Se o arquivo já existe, pula a coleta para esse repositório
            if os.path.exists(output_path):
                print(f"Arquivo {output_file} já existe. Pulando coleta para {repo}.")
                continue

            print(f"Coletando PRs do repositório: {repo}")
            prs = get_prs(repo)
            print(f"  -> Total de PRs coletados: {len(prs)}")
            save_prs_to_json(repo, prs)

if __name__ == "__main__":
    main()
