import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Paths
DATASET_PATH = "data/processed/prs_dataset.csv"
REPORT_FOLDER = "report/"

# Cria pasta report se não existir
os.makedirs(REPORT_FOLDER, exist_ok=True)

def calcular_metrica_tempo(df):
    """Calcula o tempo de análise do PR em horas"""
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['closed_at'] = pd.to_datetime(df['closed_at'])
    df['merged_at'] = pd.to_datetime(df['merged_at'])

    # Usa closed_at se merged_at for vazio
    df['end_time'] = df['merged_at'].fillna(df['closed_at'])

    df['tempo_analise_horas'] = (df['end_time'] - df['created_at']).dt.total_seconds() / 3600
    return df

def calcular_correlacoes(df):
    """Calcula correlações Spearman entre métricas"""
    colunas_interesse = ['tempo_analise_horas', 'additions', 'deletions', 'comments', 'review_comments']
    
    resultados = []

    for col1 in colunas_interesse:
        for col2 in colunas_interesse:
            if col1 != col2:
                coef, p_valor = stats.spearmanr(df[col1].fillna(0), df[col2].fillna(0))
                resultados.append({
                    'Variável 1': col1,
                    'Variável 2': col2,
                    'Coeficiente Spearman': coef,
                    'Valor-p': p_valor
                })
    return pd.DataFrame(resultados)

def plotar_graficos(df):
    """Gera gráficos e salva no diretório report/"""
    sns.set(style="whitegrid")

    # Scatter plots para tempo de análise x tamanho
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x='tempo_analise_horas', y='additions', data=df)
    plt.title("Tempo de Análise vs Linhas Adicionadas")
    plt.savefig(os.path.join(REPORT_FOLDER, "scatter_tempo_vs_additions.png"))
    plt.close()

    plt.figure(figsize=(8, 6))
    sns.scatterplot(x='tempo_analise_horas', y='deletions', data=df)
    plt.title("Tempo de Análise vs Linhas Removidas")
    plt.savefig(os.path.join(REPORT_FOLDER, "scatter_tempo_vs_deletions.png"))
    plt.close()

    # Heatmap de correlação
    plt.figure(figsize=(10, 8))
    corr = df[['tempo_analise_horas', 'additions', 'deletions', 'comments', 'review_comments']].corr(method='spearman')
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Heatmap de Correlações (Spearman)")
    plt.savefig(os.path.join(REPORT_FOLDER, "heatmap_correlacoes.png"))
    plt.close()

def main():
    df = pd.read_csv(DATASET_PATH)

    # Adiciona métricas de tempo
    df = calcular_metrica_tempo(df)

    # Calcula correlações
    df_correlacoes = calcular_correlacoes(df)
    correlacoes_path = os.path.join(REPORT_FOLDER, "correlacoes_spearman.csv")
    df_correlacoes.to_csv(correlacoes_path, index=False)
    print(f"📄 Correlações salvas em: {correlacoes_path}")

    # Gera gráficos
    plotar_graficos(df)
    print("📊 Gráficos gerados no diretório report/.")

if __name__ == "__main__":
    main()
