# https://dados.gov.br/dados/conjuntos-dados/resultado-da-arrecadacao
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df = pd.read_csv("arrecadacao-estado.csv", sep=";", encoding='utf-8')

# print(df.info())
# print(df.head())

# # LIMPEZA DE COLUNAS COM INFORMAÇÕES VAZIAS
# df.dropna(axis=1, how='all', inplace=True)

# Padronizar os números antes de convertê-los
def parse_valor(valor):
    if isinstance(valor, str):
        valor = valor.strip()
        # Corrigir formato brasileiro (milhar com ponto, decimal com vírgula)
        valor = valor.replace('.', '').replace(',', '.')
    try:
        return float(valor)
    except:
        return np.nan

# Aplica a função a todas as colunas numéricas
for col in df.columns[3:]:
    df[col] = df[col].apply(parse_valor)

# Agora calcula a coluna TOTAL_ARRECADADO
df['TOTAL_ARRECADADO'] = df[df.columns[3:]].sum(axis=1)

# PARA TESTE E COMPARAÇÃO COM EXCEL
# soma_df = df[df['UF'] == 'SP']['TOTAL_ARRECADADO'].sum()
# print(soma_df)

# Agrupar por estado (UF) e somar
arrecadacao_por_estado = df.groupby('UF')['TOTAL_ARRECADADO'].sum().sort_values(ascending=False)

# Agrupar por ano e somar
arrecadacao_por_ano = df.groupby('ANO')['TOTAL_ARRECADADO'].sum()

# Top 10 impostos por arrecadação total
top_impostos = df[[col for col in df.columns[3:] if col != 'TOTAL_ARRECADADO']].sum().sort_values(ascending=False).head(10)

# Criar gráficos
plt.figure(figsize=(14, 6))
sns.barplot(x=arrecadacao_por_estado.index, y=arrecadacao_por_estado.values, palette='viridis')
plt.title('Arrecadação Total por Estado (UF)')
plt.ylabel('R$ Arrecadado')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 5))
sns.lineplot(x=arrecadacao_por_ano.index, y=arrecadacao_por_ano.values, marker='o')
plt.title('Evolução da Arrecadação ao Longo dos Anos')
plt.ylabel('R$ Arrecadado')
plt.xlabel('Ano')
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 6))
sns.barplot(x=top_impostos.values, y=top_impostos.index, palette='magma')
plt.title('Top 10 Impostos por Valor Total Arrecadado')
plt.xlabel('R$ Arrecadado')
plt.tight_layout()
plt.show()
