import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ==========================================================
# CONFIGURAÇÃO GERAL E DA PÁGINA
# ==========================================================

if "telas" not in st.session_state:
    st.session_state.telas = "Dados"

st.title(
    "📈 Correlação e Covariância na Análise de Dados"
)

if st.sidebar.button("Tela Dados"):
    st.session_state.telas = "Dados"
if st.sidebar.button("Dados Covariância"):
    st.session_state.telas = "Dados_Covariancia"
if st.sidebar.button("Cálculo da covariância"):
    st.session_state.telas = "Calculo_Covariancia"
if st.sidebar.button("Correlação de Pearson"):
    st.session_state.telas = "Correlação_Pearson"


# ==========================================================
# 1. CARREGANDO OS DADOS
# ==========================================================

dados = pd.read_csv(
    "data.csv",
    sep=","
)

exemplo = dados[
    [   
        "tempo_entrega_min",
        "distancia_km"
    ]].copy()

# Diferença entre cada valor e a média

media_tempo = exemplo['tempo_entrega_min'].mean()
media_dist = exemplo['distancia_km'].mean()

exemplo['xi-xm'] = exemplo['tempo_entrega_min'] - media_tempo
exemplo['yi-ym'] = exemplo['distancia_km'] - media_dist
exemplo['prod'] = exemplo['xi-xm']*exemplo["yi-ym"]

# Cálculos da covariancia:

cov_manual = (
    exemplo["prod"].sum()/(exemplo.shape[0]-1)
    )

# Cálculos da correlação de Pearson:

# Elevando os desvios ao quadrado

exemplo['xi-xm_2'] = exemplo["xi-xm"]**2
exemplo['yi-ym_2'] = exemplo["yi-ym"]**2

soma_x2 = exemplo['xi-xm_2'].sum()
soma_y2 = exemplo['yi-ym_2'].sum()

prod = (soma_x2 * soma_y2)**0.5 #Tirando a raiz usasse **0.5

r_manual = exemplo['prod'].sum()/prod

if st.session_state.telas =="Dados":
    st.subheader(
        "Primeiras linhas"
    )

    st.dataframe(
        dados.head(),
        width='stretch'
    )

    # ==========================================================
    # 2. ANÁLISE EXPLORATÓRIA
    # ==========================================================

    st.header(
        "2. Análise Exploratória"
    )

    # Removendo a coluna utilizada apenas como identificador

    if "id_pedido" in dados.columns:
        dados.drop(
            columns=["id_pedido"],
            inplace=True
        )


    # ==========================================================
    # TIPOS E VALORES NULOS
    # ==========================================================

    col1, col2 = st.columns(2)


    with col1:

        st.subheader(
            "Tipos das colunas"
        )

        tipos = pd.DataFrame({
            "Coluna":
                dados.dtypes.index,
            "Tipo":
                dados.dtypes
                .astype(str)
                .values
        })


        st.dataframe(
            tipos,
            width='stretch'
        )


    with col2:

        st.subheader(
            "Valores nulos"
        )

        nulos = (
            dados
            .isna()
            .sum()
            .reset_index()
        )

        nulos.columns = [
            "Coluna",
            "Valores nulos"
        ]

        st.dataframe(
            nulos,
            width='stretch'
        )
elif st.session_state.telas == "Dados_Covariancia":
    st.header(
    "Covariância"
    )

    st.write(
        """
        A covariância mede como duas variáveis
        variam juntas.

        Vamos analisar:

        **Distância percorrida**

        versus

        **Tempo de entrega**
        """
    )
    st.subheader(
        "Dados utilizados"
    )

    st.dataframe(
        exemplo.head(10),
        width='stretch'
    )

    # ==========================================================
    # SCATTERPLOT
    # ==========================================================

    st.subheader(
        "Gráfico de Dispersão"
    )

    fig, eixo = plt.subplots(
        figsize=(8,5)
    )

    sns.scatterplot(
        data=exemplo,
        x='distancia_km',
        y='tempo_entrega_min',
        ax=eixo
    )
    eixo.set_title("Distância X Tempo de Entrega")
    eixo.set_xlabel("Distância [km]")
    eixo.set_ylabel("Tempo [min]")
    st.pyplot(fig)

elif st.session_state.telas == "Calculo_Covariancia":
    # ==========================================================
    # MÉDIAS
    # ==========================================================

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Média do tempo",
            f"{media_tempo:.2f} min"
        )
        pass

    with col2:
        st.metric(
            "Média da distância",
            f"{media_dist:.2f} km"
        )
        pass

    # ==========================================================
    # CÁLCULO MANUAL DA COVARIÂNCIA
    # ==========================================================

    st.subheader(
        "Cálculo manual da Covariância"
    )

    st.dataframe(
        exemplo.head(5),
        width='stretch'
    )

    st.metric(
        "Covariância calculada manualmente",
        f"{cov_manual:.2f}"
    )

    # ==========================================================
    # COVARIÂNCIA COM PANDAS
    # ==========================================================

    st.subheader("Covariância com o Pandas")
    cov_pandas = exemplo[[
        'distancia_km',
        'tempo_entrega_min'
    ]].cov()

    st.dataframe(
        cov_pandas,
        width='stretch'
    )

    st.write(
        """
        O método `.cov()` calcula automaticamente
        a matriz de covariância.
        """
    )
elif st.session_state.telas == "Correlação_Pearson":

    st.header(
    "Correlação de Pearson"
    )
    st.write(
        """
        A correlação de Pearson mede a força
        e a direção da relação linear entre
        duas variáveis numéricas.

        O resultado varia entre:

        **-1 e +1**
        """
    )

    st.write(
        """
        Interpretação utilizada na aula:

        - 0,00 a 0,30 → correlação fraca
        - 0,30 a 0,70 → correlação moderada
        - 0,70 a 1,00 → correlação forte

        Para valores negativos, a intensidade é
        interpretada da mesma forma, considerando
        o sinal negativo.
        """
    )

    # ==========================================================
    # CÁLCULO MANUAL DE PEARSON
    # ==========================================================

    st.subheader(
        "Cálculo manual"
    )

    st.dataframe(
        exemplo.head(5),
        width='stretch'
    )

    # ==========================================================
    # CORRELAÇÃO COM PANDAS
    # ==========================================================

    corr_pandas = exemplo[
        ['distancia_km', 
         'tempo_entrega_min']
        ].corr()

    r_pandas = corr_pandas.loc['distancia_km', 
                               'tempo_entrega_min']

    # ==========================================================
    # COMPARANDO RESULTADOS
    # ==========================================================

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Correlação Pearson - Manual",
            f"{r_manual:.4f}"
        )

    with col2:
        st.metric(
            "Correlação Pearson - Pandas",
            f"{r_pandas:.4f}"
        )

    # ==========================================================
    # INTERPRETAÇÃO
    # ==========================================================

    # [Fazer em aula]

    # ==========================================================
    # MATRIZ PARA AS DUAS VARIÁVEIS
    # ==========================================================

    st.subheader(
        "Matriz de Correlação"
    )

    st.dataframe(
        corr_pandas,
        width='stretch'
    )

    # ==========================================================
    # 6. MATRIZ DE CORRELAÇÃO GERAL
    # ==========================================================

    st.header(
        "Matriz de Correlação do DataFrame"
    )

    matriz_corr = dados.corr(
        numeric_only=True
    )

    st.dataframe(
        matriz_corr,
        width='stretch'
    )

    # ==========================================================
    # HEATMAP
    # ==========================================================

    st.subheader(
        "Heatmap da Matriz de Correlação"
    )

    fig, eixo = plt.subplots(
        figsize=(11,7)
    )
    sns.heatmap(
        data=matriz_corr,
        ax=eixo
    )
    eixo.set_title("Matrix de Correlação")
    st.pyplot(fig)