import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Dados em texto bruto
raw_data = """
803 Robert van Engelen
10 Ricardo Ribalda
6 Doug Cook
5 Doug Cook (WINDOWS)
3 Adrià Arrufat
3 Maor Gordon
3 Ricardo Ribalda Delgado
2 Ashish SHUKLA
2 Chris Moutsos
2 Daniel Lange
2 Francesco Camuffo
2 Guillaume Outters
2 Juho Pohjala
2 Pierre Rouleau
2 Ryan Caezar Itang
2 VlkrS
2 Érico Nogueira
1 Alexander Sulfrian
1 Andreas Stieger
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
plt.savefig('grafico_commitsUGREP.png', dpi=300)
# Exibe o gráfico
plt.show()