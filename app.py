import numpy as np
import pandas as pd
import streamlit as st

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Acompanhamento GP7 - Ranking & Indicadores",
    page_icon="🏆",
    layout="wide",
)

# Estilização CSS customizada para visualização de cartões e pódio
st.markdown(
    """
<style>
    .podium-box {
        text-align: center;
        padding: 15px;
        border-radius: 10px;
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        margin-bottom: 15px;
    }
    .metric-card {
        background-color: #ffffff;
        border-left: 5px solid #28a745;
        padding: 15px;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
</style>
""",
    unsafe_allow_html=True,
)


# Função para carregar os dados diretamente do Google Drive pelos IDs fornecidos
@st.cache_data(ttl=1800)  # Recarrega automaticamente o cache a cada 30 minutos
def carregar_dados():
    id_ranking = "1dmqfmNxSlnbKDOQ-H-cW1UZkq6EoV1kZ"
    id_dados = "1fpjt4DrmOjSDPYyQ-1MPr7ooZNim-1rR"

    url_ranking = (
        f"https://drive.google.com/uc?export=download&id={id_ranking}"
    )
    url_dados = f"https://drive.google.com/uc?export=download&id={id_dados}"

    df_ranking = pd.read_csv(url_ranking)
    df_detalhado = pd.read_csv(url_dados)

    return df_ranking, df_detalhado


try:
    df_ranking, df_detalhado = carregar_dados()
except Exception as e:
    st.error(
        f"Erro ao carregar os dados do Google Drive. Verifique se as permissões dos arquivos estão configuradas para 'Qualquer pessoa com o link'. Detalhes: {e}"
    )
    st.stop()

# --- BARRA LATERAL: FILTROS ---
st.sidebar.header("⚙️ Filtros de Navegação")

# Filtro por Unidade/Operação
unidades_disponiveis = ["Todas"] + list(df_ranking["Unidade"].unique())
unidade_sel = st.sidebar.selectbox("Unidade / Operação:", unidades_disponiveis)

if unidade_sel != "Todas":
    df_ranking_f = df_ranking[df_ranking["Unidade"] == unidade_sel]
    df_detalhado_f = df_detalhado[df_detalhado["Unidade"] == unidade_sel]
else:
    df_ranking_f = df_ranking.copy()
    df_detalhado_f = df_detalhado.copy()

# Filtro por Setor / RN
setores_disponiveis = ["Todos"] + sorted(
    list(df_ranking_f["Setor"].astype(str).unique())
)
setor_sel = st.sidebar.selectbox("Setor / RN:", setores_disponiveis)

if setor_sel != "Todos":
    df_ranking_f = df_ranking_f[
        df_ranking_f["Setor"].astype(str) == setor_sel
    ]
    df_detalhado_f = df_detalhado_f[
        df_detalhado_f["Setor"].astype(str) == setor_sel
    ]

# --- CABEÇALHO DO PAINEL ---
st.title("🏆 Painel de Gamificação e Performance GP7")
st.caption(
    "Acompanhamento diário de Metas, Atingimentos, Pontuação e Ranking dos RNs (Sede Jequié e Filial Itapetinga)"
)

# --- CARDS DE RESUMO ---
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Setores / RNs Exibidos", len(df_ranking_f))

with c2:
    media_pts = (
        df_ranking_f["Pontos_Acumulados"].mean()
        if not df_ranking_f.empty
        else 0
    )
    st.metric("Média de Pontos (Máx 27)", f"{media_pts:.1f} pts")

with c3:
    media_pct = (
        df_ranking_f["%_Atingimento_Pontos"].mean()
        if not df_ranking_f.empty
        else 0
    )
    st.metric("Atingimento Médio de Pontos", f"{media_pct:.1f}%")

with c4:
    elegiveis = len(
        df_ranking_f[df_ranking_f["%_Atingimento_Pontos"] >= 62.0]
    )
    st.metric("RNs Elegíveis a Selos (≥62%)", f"{elegiveis}")

st.markdown("---")

# --- ABAS DE INTERFACE ---
tab1, tab2, tab3 = st.tabs(
    ["🥇 Ranking & Selos", "📊 Metas & GAPs por Indicador", "📋 Visão Detalhada"]
)

# --- ABA 1: RANKING E PÓDIO ---
with tab1:
    st.subheader("Leaderboard do Mês")

    # Exibição do Pódio (Top 3) quando a visão geral estiver selecionada
    if len(df_ranking_f) >= 3 and setor_sel == "Todos":
        top3 = df_ranking_f.sort_values(by="Posicao").iloc[:3]
        col_p2, col_p1, col_p3 = st.columns(3)

        with col_p1:
            st.markdown(
                f"""
            <div class="podium-box" style="border-top: 5px solid #ffd700;">
                <h3>🥇 1º Lugar</h3>
                <h4>Setor {top3.iloc[0]['Setor']}</h4>
                <p><b>{top3.iloc[0]['Pontos_Acumulados']} Pts</b> ({top3.iloc[0]['%_Atingimento_Pontos']:.1f}%)</p>
                <p>{top3.iloc[0]['Selo']}</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col_p2:
            st.markdown(
                f"""
            <div class="podium-box" style="border-top: 5px solid #c0c0c0;">
                <h3>🥈 2º Lugar</h3>
                <h4>Setor {top3.iloc[1]['Setor']}</h4>
                <p><b>{top3.iloc[1]['Pontos_Acumulados']} Pts</b> ({top3.iloc[1]['%_Atingimento_Pontos']:.1f}%)</p>
                <p>{top3.iloc[1]['Selo']}</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col_p3:
            st.markdown(
                f"""
            <div class="podium-box" style="border-top: 5px solid #cd7f32;">
                <h3>🥉 3º Lugar</h3>
                <h4>Setor {top3.iloc[2]['Setor']}</h4>
                <p><b>{top3.iloc[2]['Pontos_Acumulados']} Pts</b> ({top3.iloc[2]['%_Atingimento_Pontos']:.1f}%)</p>
                <p>{top3.iloc[2]['Selo']}</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

    # Tabela completa de Ranking
    df_rank_display = df_ranking_f.copy()
    df_rank_display["%_Atingimento_Pontos"] = df_rank_display[
        "%_Atingimento_Pontos"
    ].apply(lambda x: f"{x:.1f}%")

    st.dataframe(
        df_rank_display[
            [
                "Posicao",
                "Unidade",
                "Setor",
                "Pontos_Acumulados",
                "Pontos_Possiveis",
                "%_Atingimento_Pontos",
                "Selo",
            ]
        ],
        column_config={
            "Posicao": "Posição",
            "Setor": "Setor / RN",
            "Pontos_Acumulados": "Pontos Obtidos",
            "Pontos_Possiveis": "Total Possível",
            "%_Atingimento_Pontos": "% Atingimento",
            "Selo": "Selo Conquistado",
        },
        use_container_width=True,
        hide_index=True,
    )

# --- ABA 2: RESUMO POR INDICADOR ---
with tab2:
    st.subheader("Desempenho Consolidado por Indicador")

    resumo_kpi = (
        df_detalhado_f.groupby("Indicador")
        .agg(
            Meta_Soma=("Meta", "sum"),
            Real_Soma=("Real", "sum"),
            GAP_Soma=("GAP", "sum"),
            Pontos_Soma=("Pontos", "sum"),
        )
        .reset_index()
    )

    resumo_kpi["% Atingimento Global"] = np.where(
        resumo_kpi["Meta_Soma"] > 0,
        (resumo_kpi["Real_Soma"] / resumo_kpi["Meta_Soma"]) * 100,
        0,
    )

    st.dataframe(
        resumo_kpi[
            [
                "Indicador",
                "Meta_Soma",
                "Real_Soma",
                "% Atingimento Global",
                "GAP_Soma",
                "Pontos_Soma",
            ]
        ],
        column_config={
            "Meta_Soma": st.column_config.NumberColumn(
                "Meta Total", format="%.2f"
            ),
            "Real_Soma": st.column_config.NumberColumn(
                "Realizado Total", format="%.2f"
            ),
            "% Atingimento Global": st.column_config.NumberColumn(
                "% Atingimento", format="%.1f%%"
            ),
            "GAP_Soma": st.column_config.NumberColumn(
                "GAP Total", format="%.2f"
            ),
            "Pontos_Soma": "Pontos Totais Gerados",
        },
        use_container_width=True,
        hide_index=True,
    )

# --- ABA 3: TABELA DETALHADA ---
with tab3:
    st.subheader("Matriz de Indicadores por Setor")

    st.dataframe(
        df_detalhado_f[
            [
                "Unidade",
                "Setor",
                "Indicador",
                "Base",
                "Meta",
                "Real",
                "%",
                "GAP",
                "MN",
                "Pontos",
            ]
        ],
        column_config={
            "%": st.column_config.NumberColumn("% Atingimento", format="%.1f%%"),
            "Meta": st.column_config.NumberColumn("Meta", format="%.2f"),
            "Real": st.column_config.NumberColumn("Real", format="%.2f"),
            "GAP": st.column_config.NumberColumn("GAP", format="%.2f"),
            "MN": st.column_config.NumberColumn(
                "Mínimo Diário (MN)", format="%.2f"
            ),
            "Pontos": st.column_config.NumberColumn(
                "Pontuação", format="%d pts"
            ),
        },
        use_container_width=True,
        hide_index=True,
    )
