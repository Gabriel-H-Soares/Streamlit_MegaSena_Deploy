import streamlit as st
import pandas as pd
import openpyxl

st.set_page_config( layout='wide', page_title='Mega Sena da Sorte')

if "data" not in st.session_state:
    df = pd.read_excel("datasets/Todos os resultados da Mega Sena  Rede Loteria.xlsx", header=1, index_col=0)
    df.columns = ["Data", "1º Dezena", "2º Dezena", "3º Dezena", "4º Dezena", "5º Dezena", "6º Dezena", "Ganhadores", "prêmio", "Nº de Apostas"]
    df.index.name = "Concurso"
    df['prêmio'] = df['prêmio'].apply(lambda x: round(x,0))
    df.dropna(subset=['prêmio'], inplace=True)
    df['Nº de Apostas'] = df['Nº de Apostas'].fillna(0)
    df.index = df.index.astype(int)
    st.session_state["data"] = df
        
df = st.session_state["data"]
    
st.markdown("<h1 style='color: #FF6666;'>Mega Sena</h1>", unsafe_allow_html=True)

btn = st.link_button("Acesse os dados na Rede Loteria", "https://redeloteria.com.br/mega-sena/todos-os-resultados-da-mega-sena/29275")

st.sidebar.markdown("Desenvolvido por **Gabriel Soares**")

st.dataframe(
    df,
    column_config={
        "prêmio": st.column_config.NumberColumn(
            "Prêmio",
            width=100
        )
    },
    hide_index=False
)
st.markdown(
    """
    Aqui você pode ver quais foram os maiores premios da Mega Sena, e quais foram os numeros mais sorteados.

    O dataset contém informações sobre os sorteios, desde 1996 até 2024, com detalhes como a data do sorteio, os números sorteados, 
    o valor do prêmio para o ganhador e o número de ganhadores.

    Com esse dataset, foi possível criar um dashboard interativo que permite aos usuários explorar os dados de forma fácil e intuitiva.
    Além disso, foi possível criar gráficos que mostram a frequência de cada número sorteado e a distribuição dos prêmios.

    Espero que vocês gostem!
    
"""
)