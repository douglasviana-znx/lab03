# Análise de Code Review em Projetos Open Source

## 1. Introdução

Nesta análise, buscamos entender o impacto de diferentes variáveis (tamanho dos PRs, tempo de análise, interações) no feedback final das revisões de Pull Requests em repositórios populares do GitHub.

## 2. Hipóteses

- PRs maiores tendem a ser rejeitados ou exigem mais revisões.
- PRs com maior tempo de análise têm mais interações e comentários.
- PRs com boas descrições e menos mudanças tendem a ser aceitos mais rapidamente.

## 3. Metodologia

- **Coleta** de PRs de 200 repositórios populares.
- **Filtros** aplicados:
  - PRs com status "merged" ou "closed"
  - PRs com pelo menos uma revisão
  - PRs analisados por mais de uma hora
- **Métricas** calculadas:
  - Linhas adicionadas/removidas
  - Tempo de análise em horas
  - Número de comentários e revisores

- **Correlação** analisada usando o teste de Spearman.

## 4. Resultados

### 4.1 Correlações Encontradas

*(Inserir tabela correlacoes_spearman.csv aqui)*

### 4.2 Gráficos

- Scatter plot: Tempo de análise vs Linhas adicionadas
- Scatter plot: Tempo de análise vs Linhas removidas
- Heatmap de correlações

*(Inserir imagens dos gráficos)*

## 5. Discussão

- Comentar sobre tendências observadas (ex: "PRs com mais linhas adicionadas demoraram mais para serem aprovados", etc).

## 6. Conclusão

Sumarizar as descobertas e possíveis limitações do estudo.

---
