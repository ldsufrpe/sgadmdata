import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Configuração inicial do Streamlit
st.set_page_config(page_title="Análise de Artigos Científicos", layout="wide")


# Tema do Seaborn para gráficos mais elegantes
sns.set_theme(style="whitegrid", palette="pastel")

# Função para carregar os dados
@st.cache_data
def load_data():
    df = pd.read_json('artigos.json')
    return df

df = load_data()

# Filtros interativos
st.sidebar.header('Filtros')
classificacao = st.sidebar.multiselect('Filtrar por Classificação Qualis', df['Classificação'].unique(), default=df['Classificação'].unique())
ano = st.sidebar.slider('Selecionar o Intervalo de Anos', int(df['Ano'].min()), int(df['Ano'].max()), (int(df['Ano'].min()), int(df['Ano'].max())))
area_avaliacao = st.sidebar.multiselect('Filtrar por Área de Avaliação', df['Área de Avaliação'].unique(), default=df['Área de Avaliação'].unique())

# Aplicar os filtros ao DataFrame
df_filtered = df[(df['Classificação'].isin(classificacao)) & (df['Ano'].between(ano[0], ano[1])) & (df['Área de Avaliação'].isin(area_avaliacao))]

# Cálculos estatísticos para os botões
total_artigos = df_filtered.shape[0]
media_artigos_ano = df_filtered.groupby('Ano')['ID'].count().mean()
media_fator_impacto = df_filtered['Fator de Impacto'].mean()
ano_atual = datetime.now().year
artigos_ano_atual = df_filtered[df_filtered['Ano'] == ano_atual].shape[0]

# Exibir botões no topo com informações
st.title('Análise de Artigos Científicos Publicados - Pós-Graduação')

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Artigos", total_artigos)
col2.metric("Média de Artigos por Ano", f"{media_artigos_ano:.2f}")
col3.metric("Média de Fator de Impacto", f"{media_fator_impacto:.2f}")
col4.metric(f"Artigos em {ano_atual}", artigos_ano_atual)

# Seção: Introdução
st.write("""
Essa aplicação interativa fornece insights sobre a produção científica, classificações Qualis, fator de impacto, e internacionalização dos artigos
científicos publicados. Use os filtros e gráficos interativos para explorar os dados e identificar as melhores áreas para implementar um curso de pós-graduação.
""")

# Seção: Gráficos
st.header('Visualização dos Dados')

# Layout dos gráficos
col1, col2 = st.columns(2)

# Gráfico 1: Distribuição de Artigos por Classificação Qualis
col1.subheader('Distribuição de Artigos por Classificação Qualis')
fig1, ax1 = plt.subplots(figsize=(8, 6))
classificacao_counts = df_filtered['Classificação'].value_counts().sort_index()
sns.barplot(x=classificacao_counts.index, y=classificacao_counts.values, palette='Blues_d', ax=ax1)
ax1.set_title('Distribuição por Classificação Qualis', fontsize=14)
ax1.set_xlabel('Classificação', fontsize=12)
ax1.set_ylabel('Número de Artigos', fontsize=12)
col1.pyplot(fig1)

# Gráfico 2: Fator de Impacto Médio por Classificação
col2.subheader('Fator de Impacto Médio por Classificação')
fig2, ax2 = plt.subplots(figsize=(8, 6))
impacto_medio = df_filtered.groupby('Classificação')['Fator de Impacto'].mean().sort_index()
sns.barplot(x=impacto_medio.index, y=impacto_medio.values, palette='Oranges_d', ax=ax2)
ax2.set_title('Fator de Impacto Médio por Classificação', fontsize=14)
ax2.set_xlabel('Classificação', fontsize=12)
ax2.set_ylabel('Fator de Impacto Médio', fontsize=12)
col2.pyplot(fig2)

# Gráfico 3: Proporção de Artigos com Internacionalização
st.subheader('Proporção de Artigos com Internacionalização')
fig3, ax3 = plt.subplots(figsize=(8, 6))
internacionalizacao_counts = df_filtered['Internacionalização'].value_counts(normalize=True)
internacionalizacao_counts.plot(kind='pie', autopct='%1.1f%%', colors=['#66b3ff', '#99ff99'], ax=ax3, startangle=90, wedgeprops={'edgecolor': 'white'})
ax3.set_title('Proporção de Artigos com Internacionalização', fontsize=14)
ax3.set_ylabel('')
st.pyplot(fig3)

# Gráfico 4: Distribuição de Artigos por Ano (gráfico de barras)
st.subheader('Distribuição de Artigos por Ano')
fig4, ax4 = plt.subplots(figsize=(10, 6))
artigos_por_ano = df_filtered.groupby('Ano')['ID'].count()
sns.barplot(x=artigos_por_ano.index, y=artigos_por_ano.values, palette='coolwarm', ax=ax4)
ax4.set_title('Distribuição de Artigos por Ano', fontsize=14)
ax4.set_xlabel('Ano', fontsize=12)
ax4.set_ylabel('Número de Artigos', fontsize=12)
st.pyplot(fig4)

# Gráfico 5: Fator de Impacto por Ano e por Área Específica (apenas 4 áreas principais)
st.subheader('Fator de Impacto por Ano e por Área Específica')
# Selecionar as 4 áreas com mais publicações
areas_com_mais_publicacoes = df_filtered['Área Específica'].value_counts().nlargest(4).index
df_top_areas = df_filtered[df_filtered['Área Específica'].isin(areas_com_mais_publicacoes)]
fig5, ax5 = plt.subplots(figsize=(10, 6))
sns.lineplot(data=df_top_areas, x='Ano', y='Fator de Impacto', hue='Área Específica', marker='o', palette='Set2', ax=ax5)

# Ajustar o eixo x para mostrar apenas anos inteiros
ax5.set_xticks(df_top_areas['Ano'].unique().astype(int))
ax5.set_title('Fator de Impacto por Ano e por Área Específica (Top 4 Áreas)', fontsize=14)
ax5.set_xlabel('Ano', fontsize=12)
ax5.set_ylabel('Fator de Impacto', fontsize=12)
st.pyplot(fig5)

# Gráfico 6: Fator de Impacto por Área de Avaliação
st.subheader('Fator de Impacto por Área de Avaliação')
fig6, ax6 = plt.subplots(figsize=(10, 6))
impacto_por_area = df_filtered.groupby('Área de Avaliação')['Fator de Impacto'].mean().sort_values()
sns.barplot(x=impacto_por_area.values, y=impacto_por_area.index, palette='Purples_d', ax=ax6)
ax6.set_title('Fator de Impacto por Área de Avaliação', fontsize=14)
ax6.set_xlabel('Fator de Impacto Médio', fontsize=12)
ax6.set_ylabel('Área de Avaliação', fontsize=12)
st.pyplot(fig6)

# Gráfico 7: Classificação vs. Fator de Impacto (Scatter Plot)
st.subheader('Classificação vs. Fator de Impacto')
fig7, ax7 = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=df_filtered, x='Classificação', y='Fator de Impacto', hue='Área de Avaliação', palette='coolwarm', s=100, ax=ax7)
ax7.set_title('Classificação vs. Fator de Impacto', fontsize=14)
ax7.set_xlabel('Classificação', fontsize=12)
ax7.set_ylabel('Fator de Impacto', fontsize=12)
st.pyplot(fig7)

# Gráfico 8: Artigos por Subárea Específica
st.subheader('Distribuição por Subárea Específica')
fig8, ax8 = plt.subplots(figsize=(10, 6))
subarea_counts = df_filtered['Área Específica'].value_counts()
sns.barplot(y=subarea_counts.index, x=subarea_counts.values, palette='Spectral', ax=ax8)
ax8.set_title('Distribuição por Subárea Específica', fontsize=14)
ax8.set_xlabel('Número de Artigos', fontsize=12)
ax8.set_ylabel('Área Específica', fontsize=12)
st.pyplot(fig8)

# Gráfico 9: Artigos com Internacionalização por Classificação Qualis
st.subheader('Artigos com Internacionalização por Classificação Qualis')
fig9, ax9 = plt.subplots(figsize=(10, 6))
sns.countplot(data=df_filtered, x='Classificação', hue='Internacionalização', palette='Set2', ax=ax9)
ax9.set_title('Artigos com Internacionalização por Classificação Qualis', fontsize=14)
ax9.set_xlabel('Classificação', fontsize=12)
ax9.set_ylabel('Contagem', fontsize=12)
st.pyplot(fig9)
