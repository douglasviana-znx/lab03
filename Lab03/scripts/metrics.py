import os
import json

RAW_DATA_PATH = os.path.join("data", "raw")
PROCESSED_DATA_PATH = os.path.join("data", "processed")

def extract_metrics_from_pr(pr):
    """
    Extrai métricas básicas de um PR:
      - Número do PR
      - Estado (open, closed, merged)
      - Datas de criação e fechamento/merge
      - Título
      - Usuário que abriu o PR
      - Linhas adicionadas e removidas (se disponíveis)
    """
    pr_number = pr.get("number", None)
    state = pr.get("state", None)
    merged = pr.get("merged_at", None)
    created_at = pr.get("created_at", None)
    closed_at = pr.get("closed_at", None)
    title = pr.get("title", None)
    user = pr.get("user", {}).get("login", None)
    
    additions = pr.get("additions", 0)
    deletions = pr.get("deletions", 0)
    
    metrics = {
        "pr_number": pr_number,
        "state": state,
        "merged_at": merged,
        "created_at": created_at,
        "closed_at": closed_at,
        "title": title,
        "user": user,
        "additions": additions,
        "deletions": deletions
    }
    return metrics

def process_repo_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        prs_data = json.load(f)

    metrics_list = []
    for pr in prs_data:
        metrics = extract_metrics_from_pr(pr)
        metrics_list.append(metrics)
    
    return metrics_list

def main():
    os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)
    
    for file_name in os.listdir(RAW_DATA_PATH):
        if not file_name.endswith("_prs.json"):
            continue

        file_path = os.path.join(RAW_DATA_PATH, file_name)
        print(f"Processando métricas de: {file_path}")

        metrics_list = process_repo_file(file_path)
        output_file = file_name.replace("_prs.json", "_metrics.json")
        output_path = os.path.join(PROCESSED_DATA_PATH, output_file)

        with open(output_path, "w", encoding="utf-8") as out_f:
            json.dump(metrics_list, out_f, indent=2, ensure_ascii=False)

        print(f"  -> Métricas salvas em: {output_path}")

if __name__ == "__main__":
    main()
