import streamlit as st
import pandas as pd
import seaborn as sns

# Variaveis do session state
if "telas" not in st.session_state:
    st.session_state.telas = "Tabela"

# Leitura do conjunto de dados
dados = pd.DataFrame({
    "Máquina": [
        "Motor A", "Motor B", "Motor C", "Motor D", "Motor E",
        "Motor A", "Motor B", "Motor C", "Motor D", "Motor E",
        "Motor A", "Motor B", "Motor C", "Motor D", "Motor E"
    ],
    "Turno": [
        "Manhã", "Manhã", "Manhã", "Manhã", "Manhã",
        "Tarde", "Tarde", "Tarde", "Tarde", "Tarde",
        "Noite", "Noite", "Noite", "Noite", "Noite"
    ],
    "Temperatura": [
        72, 81, 69, 90, 77,
        75, 84, 71, 87, 79,
        73, 82, 70, 92, 76
    ],
    "RPM": [
        1750, 1820, 1680, 1950, 1780,
        1760, 1850, 1700, 1920, 1800,
        1740, 1830, 1690, 1980, 1770
    ],
    "Produção": [
        120, 135, 110, 145, 128,
        125, 138, 115, 142, 130,
        118, 133, 112, 148, 126
    ]
})

# Menu lateral do projeto
st.sidebar.title("Menu")
if st.sidebar.button("📋 Tabela"):
    st.session_state.telas = "Tabela"
if st.sidebar.button("📈 Gráfico"):
    st.session_state.telas = "Gráfico"

st.title("🏭 Dados Industriais")
if st.session_state.telas == "Tabela":

    st.subheader("Tabela dos dados")
    col1, col2 = st.columns([2,1])
    with col1:
        maqs = st.multiselect("Selecione as maquinas:", dados["Máquina"].unique(), default=dados["Máquina"].unique())
    with col2:
        temp_max = st.slider("Temperatura Máxima", min_value=60, max_value=100, value=100)
    #st.write(f"Seleção: {maqs}")
    mask_maqs = ((dados['Máquina'].isin(maqs)) & (dados["Temperatura"] <= temp_max))
    st.dataframe(dados[mask_maqs])

    media_temp = dados[mask_maqs]['Temperatura'].mean()
    media_rpm = dados[mask_maqs]['RPM'].mean()
    media_prod = dados[mask_maqs]['Produção'].mean()
    std_temp = dados[mask_maqs]['Temperatura'].std()
    std_rpm = dados[mask_maqs]['RPM'].std()
    std_prod = dados[mask_maqs]['Produção'].std()

    st.subheader("📊 Resumo Estatístico")
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            st.html("""
                <h3 style="text-align:center;">
                    🌡️ Temperatura
                </h3>
            """)
            st.metric(
                "Média",
                f"{media_temp:.2f} °C"
            )
            st.metric(
                "Desvio Padrão",
                f"{std_temp:.2f} °C"
            )
    with col2:
        with st.container(border=True):
            st.html("""
                <h3 style="text-align:center;">
                    ⚙️ Rotação
                </h3>
            """)
            st.metric(
                "Média",
                f"{media_rpm:.0f} rpm"
            )
            st.metric(
                "Desvio Padrão",
                f"{std_rpm:.0f} rpm"
            )
    with col3:
        with st.container(border=True):
            st.html("""
                <h3 style="text-align:center;">
                    🏭 Produção
                </h3>
            """)
            st.metric(
                "Média",
                f"{media_prod:.1f} pçs"
            )
            st.metric(
                "Desvio Padrão",
                f"{std_prod:.1f} pçs"
            )
elif st.session_state.telas == "Gráfico":
    st.subheader("Gráficos")
    prod_maquina = dados.groupby('Máquina')['Produção'].sum()
    prod_turno = dados.groupby('Turno')['Produção'].sum()
    temp_media = dados.groupby('Máquina')['Temperatura'].sum()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.html("""
            <h3 style="text-align:center;">
                🏭 Produção por Máquina
            </h3>
        """)
        st.bar_chart(prod_maquina)
    with col2:
        st.html("""
            <h3 style="text-align:center;">
                🏭 Produção por Turno
            </h3>
        """)
        st.bar_chart(prod_turno)
    with col3:
        st.html("""
            <h3 style="text-align:center;">
                🌡️ Temperatura Média
            </h3>
        """)
        st.bar_chart(temp_media)
    grafico = sns.scatterplot(data=dados, x="RPM", y="Produção", hue="Máquina")
    st.pyplot(grafico.figure)