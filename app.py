import streamlit as st
import pandas as pd
import plotly.express as px
import io
from datetime import datetime

# --- Configuração da Página ---
st.set_page_config(
    page_title="Dashboard de Salários na Área de Dados",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Upload do arquivo CSV ---
st.sidebar.header("📁 Selecione um arquivo CSV")
arquivo_csv = st.sidebar.file_uploader("Escolha o arquivo", type="csv")
st.sidebar.markdown("⚠️ O arquivo deve ser `.csv` e ter no máximo **200MB**.")
# --- Exemplo de estrutura esperada ---
st.sidebar.markdown("📄 **Modelo esperado do arquivo CSV:**")
st.sidebar.code(
    "ano,senioridade,contrato,cargo,salario,moeda,usd,residencia,remoto,empresa,tamanho_empresa,residencia_iso3\n"
    "2025,senior,integral,Solutions Engineer,214000,USD,214000,US,remoto,US,media,USA",
    language="csv"
)


if arquivo_csv is not None:
    df = pd.read_csv(arquivo_csv)

    # --- Barra Lateral (Filtros) ---
    st.sidebar.header("🔍 Filtros")

    anos_disponiveis = sorted(df['ano'].dropna().unique())
    anos_selecionados = st.sidebar.multiselect("Ano", anos_disponiveis, default=anos_disponiveis)

    senioridades_disponiveis = sorted(df['senioridade'].dropna().unique())
    senioridades_selecionadas = st.sidebar.multiselect("Senioridade", senioridades_disponiveis, default=senioridades_disponiveis)

    contratos_disponiveis = sorted(df['contrato'].dropna().unique())
    contratos_selecionados = st.sidebar.multiselect("Tipo de Contrato", contratos_disponiveis, default=contratos_disponiveis)

    tamanhos_disponiveis = sorted(df['tamanho_empresa'].dropna().unique())
    tamanhos_selecionados = st.sidebar.multiselect("Tamanho da Empresa", tamanhos_disponiveis, default=tamanhos_disponiveis)

    # --- Filtragem do DataFrame ---
    df_filtrado = df[
        (df['ano'].isin(anos_selecionados)) &
        (df['senioridade'].isin(senioridades_selecionadas)) &
        (df['contrato'].isin(contratos_selecionados)) &
        (df['tamanho_empresa'].isin(tamanhos_selecionados))
    ]

    # --- Conteúdo Principal ---
    st.title("🎲 Dashboard de Análise de Salários na Área de Dados")
    st.markdown("Explore os dados salariais na área de dados nos últimos anos. Utilize os filtros à esquerda para refinar sua análise.")

    # --- Métricas Principais ---
    st.subheader("📌 Métricas gerais (Salário anual em USD)")

    if not df_filtrado.empty:
        salario_medio = df_filtrado['usd'].mean()
        salario_mediano = df_filtrado['usd'].median()
        salario_maximo = df_filtrado['usd'].max()
        total_registros = df_filtrado.shape[0]
        cargo_mais_frequente = df_filtrado["cargo"].mode()[0]
    else:
        salario_medio, salario_mediano, salario_maximo, total_registros, cargo_mais_frequente = 0, 0, 0, 0 ,"" ,""

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("💰 Salário médio", f"${salario_medio:,.0f}")
    col2.metric("🔢 Salário mediano", f"${salario_mediano:,.0f}")
    col3.metric("📈 Salário máximo", f"${salario_maximo:,.0f}")
    col4.metric("🧾 Total de registros", f"{total_registros:,}")
    col5.metric("👨‍💻 Cargo mais frequente", cargo_mais_frequente)

    st.markdown("---")

    # --- Gráficos ---
    with st.expander("📊 Gráficos de Análise", expanded=True):
        
        col_graf1, col_graf2 = st.columns(2)
        with col_graf1:
            if not df_filtrado.empty:
                top_cargos = df_filtrado.groupby('cargo')['usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
                grafico_cargos = px.bar(
                    top_cargos,
                    x='usd',
                    y='cargo',
                    orientation='h',
                    title="Top 10 cargos por salário médio",
                    labels={'usd': 'Média salarial anual (USD)', 'cargo': ''}
                )
                grafico_cargos.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(grafico_cargos, use_container_width=True)
            else:
                st.warning("⚠️ Nenhum dado para exibir no gráfico de cargos.")

        with col_graf2:
            if not df_filtrado.empty:
                grafico_hist = px.histogram(
                    df_filtrado,
                    x='usd',
                    nbins=30,
                    title="Distribuição de salários anuais",
                    labels={'usd': 'Faixa salarial (USD)', 'count': ''}
                )
                grafico_hist.update_layout(title_x=0.1)
                st.plotly_chart(grafico_hist, use_container_width=True)
            else:
                st.warning("⚠️ Nenhum dado para exibir no gráfico de distribuição.")

        col_graf3, col_graf4 = st.columns(2)
        with col_graf3:
            if not df_filtrado.empty:
                remoto_contagem = df_filtrado['remoto'].value_counts().reset_index()
                remoto_contagem.columns = ['tipo_trabalho', 'quantidade']
                grafico_remoto = px.pie(
                    remoto_contagem,
                    names='tipo_trabalho',
                    values='quantidade',
                    title='Proporção dos tipos de trabalho',
                    hole=0.5
                )
                grafico_remoto.update_traces(textinfo='percent+label')
                grafico_remoto.update_layout(title_x=0.1)
                st.plotly_chart(grafico_remoto, use_container_width=True)
            else:
                st.warning("⚠️ Nenhum dado para exibir no gráfico dos tipos de trabalho.")

        with col_graf4:
            if not df_filtrado.empty:
                df_ds = df_filtrado[df_filtrado['cargo'] == 'Data Scientist']
                media_ds_pais = df_ds.groupby('residencia_iso3')['usd'].mean().reset_index()
                grafico_paises = px.choropleth(
                    media_ds_pais,
                    locations='residencia_iso3',
                    color='usd',
                    color_continuous_scale='rdylgn',
                    title='Salário médio de Cientista de Dados por país',
                    labels={'usd': 'Salário médio (USD)', 'residencia_iso3': 'País'}
                )
                grafico_paises.update_layout(title_x=0.1)
                st.plotly_chart(grafico_paises, use_container_width=True)
            else:
                st.warning("⚠️ Nenhum dado para exibir no gráfico de países.")

        # Gráfico de evolução salarial por ano
        if not df_filtrado.empty:
            grafico_evolucao = px.line(
                df_filtrado.groupby('ano')['usd'].mean().reset_index(),
                x='ano',
                y='usd',
                markers=True,
                title="📅 Evolução do salário médio por ano",
                labels={'usd': 'Salário médio (USD)', 'ano': 'Ano'}
            )
            grafico_evolucao.update_layout(title_x=0.1)
            st.plotly_chart(grafico_evolucao, use_container_width=True)
        else:
            st.warning("⚠️ Nenhum dado para exibir no gráfico de evolução salarial.")

        # Gráfico de distribuição por senioridade
        if not df_filtrado.empty:
            grafico_disp = px.box(
                df_filtrado,
                x='senioridade',
                y='usd',
                color='senioridade',
                color_discrete_map={
                    'junior': '#1f77b4',
                    'pleno': '#ff7f0e',
                    'senior': '#2ca02c',
                    'executivo': '#d62728'
                },
                title="📊 Distribuição salarial por senioridade",
                labels={'usd': 'Salário (USD)', 'senioridade': 'Senioridade'}
            )
            grafico_disp.update_layout(title_x=0.1)
            st.plotly_chart(grafico_disp, use_container_width=True)
        else:
            st.warning("⚠️ Nenhum dado para exibir no gráfico de distribuição por senioridade.")

    st.markdown("---")

    # --- Tabela de Dados Detalhados ---
    st.subheader("📋 Dados Detalhados")
    st.dataframe(df_filtrado)

    with st.spinner("⏳ Gerando arquivo para download em xlsx..."):
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df_filtrado.to_excel(writer, index=False, sheet_name='Dados')
        buffer.seek(0)

    st.success("✅ Arquivo pronto para download em xlsx!")

    st.download_button(
        label="📥 Baixar dados filtrados 🧾 (xlsx)",
        data=buffer,
        file_name='dados_filtrados_' + datetime.now().strftime('%d-%m-%YT%H-%M') + '.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    # --- Rodapé ---
    st.markdown("---")
    st.caption("📌 Faça upload de um arquivo CSV com colunas compatíveis para visualizar os dados.")
else:
    st.title("📁 Dashboard de Salários na Área de Dados")
    st.markdown("Por favor, selecione um arquivo CSV na barra lateral para iniciar a análise.")
