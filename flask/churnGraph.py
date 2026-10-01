import matplotlib.pyplot as plt
import pandas as pd

# Dados fornecidos
dados_raw = """    
uv.lock                                            7442         4358         11800       
tests/test_basic.py                                4266         3670         7936        
flask/app.py                                       4408         1997         6405        
src/flask/app.py                                   3417         2013         5430        
tests/flask_tests.py                               2703         2556         5259        
tests/test_helpers.py                              2118         2400         4518        
CHANGES.rst                                        2612         1722         4334        
flask.py                                           2205         2069         4274        
docs/quickstart.rst                                2289         1430         3719        
flask/cli.py                                       2096         1131         3227
"""

# Processamento dos dados
linhas = dados_raw.strip().split('\n')
lista_dados = []
for l in linhas:
    partes = l.split()
    lista_dados.append({
        'arquivo': partes[0],
        'insercoes': int(partes[1]),
        'delecoes': int(partes[2]),
        'total': int(partes[3])
    })

df = pd.DataFrame(lista_dados).iloc[::-1].reset_index(drop=True)

# Plot
plt.figure(figsize=(12, 7))

# Barras empilhadas
plt.barh(df['arquivo'], df['insercoes'], label='Inserções (+)', color='#2ecc71', height=0.65)
plt.barh(df['arquivo'], df['delecoes'], left=df['insercoes'], label='Deleções (-)', color='#e74c3c', height=0.65)

# Adicionar os valores numéricos em cada segmento
for i, row in df.iterrows():
    inc = row['insercoes']
    dec = row['delecoes']
    tot = row['total']
    
    # Rótulo de inserções (dentro da barra verde)
    if inc > 500:
        plt.text(inc / 2, i, f"{inc:,}".replace(",", "."), va='center', ha='center', fontsize=8.5, fontweight='bold', color='white')
        
    # Rótulo de deleções (dentro da barra vermelha)
    if dec > 500:
        plt.text(inc + (dec / 2), i, f"{dec:,}".replace(",", "."), va='center', ha='center', fontsize=8.5, fontweight='bold', color='white')
        
    # Rótulo do total (ao lado da barra)
    plt.text(tot + 300, i, f"{tot:,}".replace(",", "."), va='center', ha='left', fontsize=9, fontweight='bold', color='#333333')

plt.title('Top 10 Arquivos com Maior Volatilidade de Código (Churn)', fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Volume Total de Linhas Alteradas', fontsize=11, labelpad=10)
plt.ylabel('Caminho do Arquivo', fontsize=11, labelpad=10)

plt.xlim(0, max(df['total']) * 1.15)
plt.legend(loc='lower right', frameon=True, facecolor='white', edgecolor='none')
plt.grid(axis='x', linestyle='--', alpha=0.4)
plt.tight_layout()

plt.savefig('grafico_churn_Flask.png', dpi=300)
plt.show()