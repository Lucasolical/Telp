import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#Objetivo: Analisar o quanto o codigo está centralizado em apenas uma pessoa
# 1. Dados em texto bruto
raw_data = """
501	 zlixine moro
281	 Ahmed Saied
8 v7medz
"""

# 2. Processamento do texto para um DataFrame
data = []
for line in raw_data.strip().split('\n'):
    parts = line.strip().split(' ', 1)
    commits = int(parts[0])
    author = parts[1]
    data.append({'Autor': author, 'Commits': commits})

df = pd.DataFrame(data)

# 3. Configuração do gráfico
plt.figure(figsize=(10, 8))
sns.set_theme(style="whitegrid")

# Destaca o maior contribuidor com uma cor diferente
colors = ['#d62728' if c == df['Commits'].max() else '#1f77b4' for c in df['Commits']]

# Gráfico de barras horizontais
ax = sns.barplot(data=df, x='Commits', y='Autor', palette=colors)

# Usando escala logarítmica para lidar com o grande outlier (803 vs 12)
plt.xscale('log')

# Títulos e rótulos
plt.title('Quantidade de Commits por Pessoa', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Número de Commits (Escala Logarítmica)', fontsize=12)
plt.ylabel('Autor', fontsize=12)

# Adiciona os valores numéricos ao lado de cada barra
for p in ax.patches:
    width = p.get_width()
    if width > 0:
        ax.annotate(f'{int(width)}',
                    (width, p.get_y() + p.get_height() / 2.),
                    ha='left', va='center',
                    xytext=(6, 0),
                    textcoords='offset points',
                    fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('grafico_commitsNuclear.png', dpi=300)
# Exibe o gráfico
plt.show()