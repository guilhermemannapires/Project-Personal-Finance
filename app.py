import streamlit as st
import pandas as pd
import plotly_express as px
import datetime

st.set_page_config(layout="wide")

df = pd.read_excel('despesas.xlsx')

st.title('Personal Finance')

# 2 variáveis idenficando a data inicial do filtro e a data final, para colocarmos no filtro de range time.
min_date = datetime.date(2021, 1, 1)
max_date = datetime.date(2022, 12, 31)

# Criamos a imagem do cliente na sidebar.
st.sidebar.image("imagens/img_hom.png", caption="Name: Guilherme")

# Parte final da criação do filtro de calendário, que controlará todo dashboard pelo range de time.
calendario = st.sidebar.date_input('Choose the period: ', (min_date, max_date))

calendario_inicio = pd.to_datetime(calendario[0])
calendario_fim = pd.to_datetime(calendario[1])

calendario_filtro = df[(df["Data"] >= calendario_inicio)
                       & (df["Data"] <= calendario_fim)]

# Criar as duas métricas de ativo e passivo. (Lembrando que dentro do calendario_filtro está toda tabela despesas, mas filtrada pela data que definimos)
ganhos = calendario_filtro[calendario_filtro["Valor"] >= 1]["Valor"].sum()
perdas = calendario_filtro[calendario_filtro["Valor"] <= -1]["Valor"].sum()

col1, col2, col3, col4 = st.columns(4)
col1.image("imagens/money_up.png", width=90)
col2.metric("Income", ganhos)
col3.image("imagens/money_down.png", width=90)
col4.metric("Expenses", perdas)

st.divider()

# Criar bar com plotly
st.title("Total graph of income and expenses")

fig = px.bar(calendario_filtro, x="Categoria", y="Valor", color="Descrição")
fig

st.divider()

# Criar gráfico com plotly com um multiselect
# Primeiro o multiselect das descrições

st.title("Filter expenses by income separately")

opcoes_descricao = calendario_filtro["Descrição"].unique()
descricao_selecionada = st.multiselect(
    "Select the descriptions: ", opcoes_descricao)

calendario_filtro_descricao = calendario_filtro[calendario_filtro["Descrição"].isin(
    descricao_selecionada)]

# Criar gráfico de visualização separadamente dos ativos com cada passivo

fig2 = px.bar(calendario_filtro_descricao, x="Descrição", y="Valor")
fig2
