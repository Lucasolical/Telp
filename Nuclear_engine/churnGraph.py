import matplotlib.pyplot as plt
import pandas as pd

# Dados fornecidos
dados_raw = """      
Deps/GLEW/include/glew.h                           39506        39506        79012       
Nuclear.Engine/Source/ThirdParty/angelscript/source/as_compiler.cpp 0            16517        16517       
Nuclear.Engine/include/ThirdParty/zpp_bits.h       11030        4553         15583       
Samples/Sample2.h                                  5940         5815         11755       
Samples/Sample1.h                                  4140         3791         7931        
Deps/GLEW/include/glxew.h                          3544         3544         7088        
Nuclear.Engine/Source/Engine/Graphics/ImGUI/imgui.cpp 6521         533          7054        
Samples/Assets/Common/Textures/HDR/newport_loft.hdr 3354         3354         6708        
Nuclear.Engine/Source/ThirdParty/angelscript/source/as_scriptengine.cpp 0            6614         6614
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

plt.savefig('grafico_churn_Nuclear.png', dpi=300)
plt.show()