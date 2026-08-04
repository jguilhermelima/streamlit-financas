import pandas as pd
import streamlit as st

st.set_page_config(page_title="Finanças", page_icon="💰")

st.markdown(""" \
# Boas Vindas!

## Nosso APP de Financeiro
""")
# widget de upload de dados
file_upload = st.file_uploader(label="Faça upload dos dados aqui", type=["csv"])
# Verifica se algum arquivo foi feito upload
if file_upload:
    # leitura dos dados
    df = pd.read_csv(file_upload)
    df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y").dt.date

    # exibição dos dados no App
    exp1 = st.expander("Dados Brutos")
    colums_fmt = {"Valor": st.column_config.NumberColumn("Valor", format="R$ %f")}
    exp1.dataframe(df, hide_index=True, column_config=colums_fmt)

    # visão instituição
    exp2 = st.expander("Instituições")
    df_instituicao = df.pivot_table(index="Data", columns="Instituição", values="Valor")

    tab_data, tab_history, tab_share = exp2.tabs(["Dados", "Histórico", "Distribuição"])

    # duas maneiras de usar tab uma direta e outra com with
    tab_data.dataframe(df_instituicao)

    with tab_history:
        st.line_chart(df_instituicao)

    with tab_share:
        # # Uma maneira de selecionar data com calendario para plotar grafico
        # date = st.date_input(
        #     "Data para Distribuição",
        #     min_value=df_instituicao.index.min(),
        #     max_value=df_instituicao.index.max(),
        # )

        # if date not in df_instituicao.index:
        #     st.warning("Entre com uma data válida")
        # else:
        #     st.bar_chart(df_instituicao.loc[date])

        # Segunda maneira utilizando um selectbox apenas com as datas do df
        date = st.selectbox("Filtro Data", options=df_instituicao.index)
        st.bar_chart(df_instituicao.loc[date])
