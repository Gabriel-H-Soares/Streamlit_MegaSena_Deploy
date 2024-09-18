import streamlit as st
import altair as alt

st.set_page_config(layout='wide', page_title='Estatísticas da Mega Sena')

df_Stat = st.session_state["data"]

# Contar a frequência de cada dezena
dezenas = df_Stat[["1º Dezena", "2º Dezena", "3º Dezena", "4º Dezena", "5º Dezena", "6º Dezena"]].melt()
frequencia_dezenas = dezenas['value'].value_counts().reset_index()
frequencia_dezenas.columns = ['Números', 'Frequência']


# Calcular a porcentagem de cada dezena
frequencia_dezenas['Porcentagem'] = (frequencia_dezenas['Frequência'] / frequencia_dezenas['Frequência'].sum()) * 100
frequencia_dezenas['Porcentagem'] = frequencia_dezenas['Porcentagem'].apply(lambda x: round(x,2))


# Ordenar o dataframe pela frequência
frequencia_dezenas = frequencia_dezenas.sort_values(by='Frequência', ascending=False).reset_index(drop=True)
frequencia_dezenas.set_index('Frequência', inplace=True)

st.markdown("<h1 style='color: #FF6666;'>Estatísticas da Mega Sena</h1>", unsafe_allow_html=True)
st.markdown(
    """
    Aqui você pode ver a distribuição dos prêmios da Mega Sena.
"""
)
chart = alt.Chart(df_Stat.reset_index()).mark_bar().encode(
    x=alt.X('Data:T',axis=alt.Axis(title=None)),
    y=alt.Y('prêmio:Q', axis=alt.Axis(title=None, format=',.0f'))  # Formato com separador de milhar
).properties(
    width=800,
    height=400
)

st.altair_chart(chart, use_container_width=True)

col1, col2, col3 = st.columns([3, 2, 1])

with col1:
    st.markdown(
            """
            O Percentual de frequência de sorteio de cada número de jogos vencedores.
        """
        )
    # Exibir o novo dataframe
    st.dataframe(frequencia_dezenas,
                    column_config={
                        "Porcentagem": st.column_config.ProgressColumn(
                            "Porcentagem", format="%.2f", min_value=0, max_value=frequencia_dezenas['Porcentagem'].max())
                        })
# Após exibir o dataframe da frequência
with col2:
    st.markdown("## Gerador de Combinações")

    # Adicionar um slider para que o Lázarente escolha o intervalo de porcentagem
    percentage_range = st.slider(
        "Escolha o intervalo de saída dos números",
        frequencia_dezenas['Porcentagem'].min(),
        frequencia_dezenas['Porcentagem'].max(),
        (frequencia_dezenas['Porcentagem'].min(), frequencia_dezenas['Porcentagem'].max())
    )
    min_percentage, max_percentage = percentage_range
    # Adicionar um número para que o Lázarente escolha quantas combinações quer gerar
    num_combinations = st.number_input("Quantas combinações você deseja gerar?", min_value=1, max_value=10, value=1, step=1)

    # Botão para gerar combinações
    if st.button("Gerar Combinações"):
       filtered_numbers = frequencia_dezenas[
            (frequencia_dezenas['Porcentagem'] >= min_percentage) & 
            (frequencia_dezenas['Porcentagem'] <= max_percentage)
        ]
        # Gerador de combinações
       for i in range(num_combinations):
            if len(filtered_numbers) > 6:
                combination = filtered_numbers['Números'].sample(6, replace=False).tolist()
                combination.sort()  # Ordenar a lista diretamente
                styled_numbers = " ".join([f'<span style="display: inline-block; width: 30px; height: 30px; line-height: 30px; text-align: center; background-color: #FF6666; color: white; border-radius: 50%; margin-right: 5px;">{num}</span>' for num in combination])
                
                st.markdown(f"Combinação {i+1}: {styled_numbers}", unsafe_allow_html=True)
            else:
                st.write(f"Não há números suficientes para gerar a combinação. Tente alterar o intervalo.")
                break

with col3:
    st.empty()
                        