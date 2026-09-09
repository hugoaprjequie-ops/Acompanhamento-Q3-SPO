import numpy as np
import pandas as pd
import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Incentivo SPO Q3 - Performance & Gamificação",
    page_icon="🏆",
    layout="wide",
)

# --- CSS MODERNO E AJUSTES DE TIPOGRAFIA PARA PRINT ---
st.markdown(
    """
<style>
    /* Estilo Geral */
    .stApp {
        background-color: #f4f6f9;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Header Principal */
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .main-header h1 {
        color: #ffffff !important;
        font-weight: 800;
        margin: 0;
        font-size: 2.2rem;
    }
    .main-header p {
        color: #e0e6ed;
        margin-top: 5px;
        font-size: 1rem;
    }

    /* Podium Cards */
    .podium-box {
        text-align: center;
        padding: 20px;
        border-radius: 12px;
        background: #ffffff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #e1e8ed;
    }

    /* Container Customizado de Tabela HTML para Alta Visibilidade em Print */
    .table-container-print {
        width: 100%;
        overflow-x: auto;
        background: #ffffff;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #e1e8ed;
    }

    .styled-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 13px !important; /* Tipografia Aumentada */
        font-family: Arial, sans-serif;
    }

    .styled-table th {
        background-color: #1e3c72 !important;
        color: #ffffff !important;
        font-weight: bold;
        text-align: center;
        padding: 8px 6px;
        border: 1px solid #dcdcdc;
    }

    .styled-table td {
        padding: 6px 4px;
        text-align: center;
        border: 1px solid #e2e8f0;
        font-weight: 500;
        color: #2d3748;
    }

    /* Estilo de Impressão/Print */
    @media print {
        .stSidebar, .stTabs [data-baseweb="tab-list"] { display: none; }
        .styled-table { font-size: 11px !important; }
    }
</style>
""",
    unsafe_allow_html=True,
)


# --- CARREGAMENTO DE DADOS ---
@st.cache_data(ttl=60)
def carregar_dados():
  id_ranking = "1dmqfmNxSlnbKDOQ-H-cW1UZkq6EoV1kZ"
  id_dados = "1fpjt4DrmOjSDPYyQ-1MPr7ooZNim-1rR"

  url_ranking = (
      f"https://drive.google.com/uc?export=download&id={id_ranking}"
  )
  url_dados = f"https://drive.google.com/uc?export=download&id={id_dados}"

  df_ranking = pd.read_csv(url_ranking)
  df_detalhado = pd.read_csv(url_dados)

  SETORES_GV2 = [
      "201",
      "202",
      "203",
      "204",
      "205",
      "206",
      "207",
      "208",
      201,
      202,
      203,
      204,
      205,
      206,
      207,
      208,
  ]

  if "GV" not in df_ranking.columns:
    df_ranking["GV"] = np.where(
        df_ranking["Setor"].astype(str).isin([str(x) for x in SETORES_GV2]),
        "GV 2",
        "GV 1",
    )

  if "GV" not in df_detalhado.columns:
    df_detalhado["GV"] = np.where(
        df_detalhado["Setor"].astype(str).isin([str(x) for x in SETORES_GV2]),
        "GV 2",
        "GV 1",
    )

  return df_ranking, df_detalhado


try:
  df_ranking, df_detalhado = carregar_dados()
except Exception as e:
  st.error(f"Erro ao carregar os dados: {e}")
  st.stop()

KPIS_OFICIAIS = [
    "Rotina +",
    "Aderência de Política Comercial",
    "Execução Menu",
    "Tasks de Faturamento Score 5",
    "Tarefas de NAB TT (apenas Portfolio)",
    "Tarefa de SKU/PDV TT",
    "Tarefa de Cerveja Zero (apenas portfolio)",
    "Tarefa de Digitalização",
    "Atendimento Produtivo",
    "Lojas Ideais",
]

KPIS_PERCENTUAIS = [
    "Execução Menu",
    "Tarefa de Digitalização",
    "Aderência de Política Comercial",
    "Lojas Ideais",
]

# --- FILTROS DE NAVEGAÇÃO NA SIDEBAR ---
st.sidebar.header("⚙️ Filtros de Navegação")

unidades_disponiveis = ["Todas"] + list(df_ranking["Unidade"].unique())
unidade_sel = st.sidebar.selectbox("Unidade / Operação:", unidades_disponiveis)

if unidade_sel != "Todas":
  df_ranking_f = df_ranking[df_ranking["Unidade"] == unidade_sel]
  df_detalhado_f = df_detalhado[df_detalhado["Unidade"] == unidade_sel]
else:
  df_ranking_f = df_ranking.copy()
  df_detalhado_f = df_detalhado.copy()

gvs_disponiveis = ["Todas"] + sorted(
    list(df_ranking_f["GV"].dropna().astype(str).unique())
)
gv_sel = st.sidebar.selectbox("Gerência de Vendas (GV):", gvs_disponiveis)

if gv_sel != "Todas":
  df_ranking_f = df_ranking_f[df_ranking_f["GV"] == gv_sel]
  df_detalhado_f = df_detalhado_f[df_detalhado_f["GV"] == gv_sel]

setores_disponiveis = ["Todos"] + sorted(
    list(df_ranking_f["Setor"].astype(str).unique())
)
setor_sel = st.sidebar.selectbox("Setor / RN:", setores_disponiveis)

if setor_sel != "Todos":
  df_ranking_f = df_ranking_f[df_ranking_f["Setor"].astype(str) == setor_sel]
  df_detalhado_f = df_detalhado_f[
      df_detalhado_f["Setor"].astype(str) == setor_sel
  ]

df_ranking_f = df_ranking_f.sort_values(
    by=["%_Atingimento_Pontos", "Pontos_Acumulados"], ascending=False
).reset_index(drop=True)
df_ranking_f["Posicao"] = df_ranking_f.index + 1

# --- CABEÇALHO PRINCIPAL ---
st.markdown(
    """
    <div class="main-header">
        <h1>🏆 Incentivo SPO Q3</h1>
        <p>Acompanhamento diário de Metas, Atingimentos, Pontuação e Ranking dos RNs</p>
    </div>
""",
    unsafe_allow_html=True,
)

# --- METRIC CARDS ---
c1, c2, c3, c4 = st.columns(4)

with c1:
  st.metric("Setores / RNs Exibidos", len(df_ranking_f))

with c2:
  media_pts = (
      df_ranking_f["Pontos_Acumulados"].mean() if not df_ranking_f.empty else 0
  )
  st.metric("Média de Pontos (Máx 27)", f"{media_pts:.1f} pts")

with c3:
  media_pct = (
      df_ranking_f["%_Atingimento_Pontos"].mean()
      if not df_ranking_f.empty
      else 0
  )
  st.metric("Atingimento Médio", f"{media_pct:.1f}%")

with c4:
  elegiveis = len(df_ranking_f[df_ranking_f["%_Atingimento_Pontos"] >= 62.0])
  st.metric("RNs Elegíveis a Selos (≥62%)", f"{elegiveis}")

st.markdown("<br>", unsafe_allow_html=True)

# --- NAVEGAÇÃO DE ABAS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "🥇 Ranking & Selos",
    "📊 Metas & GAPs por Indicador",
    "📋 Visão Detalhada",
    "📌 Consolidado por RN",
])

# --- TAB 1: RANKING ---
with tab1:
  st.subheader("Leaderboard do Mês")

  if len(df_ranking_f) >= 3 and setor_sel == "Todos":
    top3 = df_ranking_f.sort_values(by="Posicao").iloc[:3]
    col_p2, col_p1, col_p3 = st.columns(3)

    with col_p1:
      st.markdown(
          f"""
            <div class="podium-box" style="border-top: 5px solid #ffd700;">
                <h3 style="color:#d4af37; margin:0;">🥇 1º Lugar</h3>
                <h4 style="margin:8px 0;">Setor {top3.iloc[0]['Setor']} ({top3.iloc[0]['GV']})</h4>
                <p style="font-size:1.1rem; margin:0;"><b>{top3.iloc[0]['Pontos_Acumulados']} Pts</b> ({top3.iloc[0]['%_Atingimento_Pontos']:.1f}%)</p>
                <p style="margin-top:5px;">{top3.iloc[0]['Selo']}</p>
            </div>
            """,
          unsafe_allow_html=True,
      )

    with col_p2:
      st.markdown(
          f"""
            <div class="podium-box" style="border-top: 5px solid #c0c0c0;">
                <h3 style="color:#8a8a8a; margin:0;">🥈 2º Lugar</h3>
                <h4 style="margin:8px 0;">Setor {top3.iloc[1]['Setor']} ({top3.iloc[1]['GV']})</h4>
                <p style="font-size:1.1rem; margin:0;"><b>{top3.iloc[1]['Pontos_Acumulados']} Pts</b> ({top3.iloc[1]['%_Atingimento_Pontos']:.1f}%)</p>
                <p style="margin-top:5px;">{top3.iloc[1]['Selo']}</p>
            </div>
            """,
          unsafe_allow_html=True,
      )

    with col_p3:
      st.markdown(
          f"""
            <div class="podium-box" style="border-top: 5px solid #cd7f32;">
                <h3 style="color:#b06d29; margin:0;">🥉 3º Lugar</h3>
                <h4 style="margin:8px 0;">Setor {top3.iloc[2]['Setor']} ({top3.iloc[2]['GV']})</h4>
                <p style="font-size:1.1rem; margin:0;"><b>{top3.iloc[2]['Pontos_Acumulados']} Pts</b> ({top3.iloc[2]['%_Atingimento_Pontos']:.1f}%)</p>
                <p style="margin-top:5px;">{top3.iloc[2]['Selo']}</p>
            </div>
            """,
          unsafe_allow_html=True,
      )
    st.markdown("<br>", unsafe_allow_html=True)

  df_rank_display = df_ranking_f.copy()
  df_rank_display["%_Atingimento_Pontos"] = df_rank_display[
      "%_Atingimento_Pontos"
  ].apply(lambda x: f"{x:.1f}%")

  st.dataframe(
      df_rank_display[[
          "Posicao",
          "Unidade",
          "GV",
          "Setor",
          "Pontos_Acumulados",
          "Pontos_Possiveis",
          "%_Atingimento_Pontos",
          "Selo",
      ]],
      column_config={
          "Posicao": "Posição",
          "GV": "GV",
          "Setor": "Setor / RN",
          "Pontos_Acumulados": "Pontos Obtidos",
          "Pontos_Possiveis": "Total Possível",
          "%_Atingimento_Pontos": "% Atingimento",
          "Selo": "Selo Conquistado",
      },
      use_container_width=True,
      hide_index=True,
  )

# --- TAB 2: METAS E GAPS POR INDICADOR ---
with tab2:
  st.subheader("Desempenho Consolidado por Indicador")

  df_kpi_filtered = df_detalhado_f[
      df_detalhado_f["Indicador"].isin(KPIS_OFICIAIS)
  ].copy()

  list_kpi_resumo = []
  for ind in KPIS_OFICIAIS:
    group = df_kpi_filtered[df_kpi_filtered["Indicador"] == ind]
    if group.empty:
      continue

    is_pct = ind in KPIS_PERCENTUAIS

    if is_pct:
      meta_val = group["Meta"].mean()
      real_val = group["Real"].mean()
      meta_fmt = f"{meta_val:.1f}%".replace(".", ",")
      real_fmt = f"{real_val:.1f}%".replace(".", ",")
      gap_fmt = f"{max(meta_val - real_val, 0):.1f}%".replace(".", ",")
    elif ind == "Rotina +":
      meta_val = 27.0
      real_val = group["Real"].sum()
      meta_fmt = "27,00"
      real_fmt = f"{int(real_val)},00"
      gap_fmt = f"{max(meta_val - real_val, 0):.2f}".replace(".", ",")
    else:
      meta_val = group["Meta"].sum()
      real_val = group["Real"].sum()
      meta_fmt = f"{meta_val:.2f}".replace(".", ",")
      real_fmt = f"{real_val:.2f}".replace(".", ",")
      gap_fmt = f"{max(meta_val - real_val, 0):.2f}".replace(".", ",")

    ating_val = (real_val / meta_val * 100) if meta_val > 0 else 0
    pts_val = group["Pontos"].sum()

    list_kpi_resumo.append({
        "Indicador": ind,
        "Meta Total": meta_fmt,
        "Realizado Total": real_fmt,
        "% Atingimento": f"{ating_val:.1f}%".replace(".", ","),
        "GAP Total": gap_fmt,
        "Pontos Totais Gerados": int(pts_val),
    })

  df_resumo_final = pd.DataFrame(list_kpi_resumo)
  st.dataframe(df_resumo_final, use_container_width=True, hide_index=True)

# --- TAB 3: VISÃO DETALHADA ---
with tab3:
  st.subheader("Matriz de Indicadores por Setor")

  df_vis_det = df_detalhado_f.copy()
  df_vis_det["Meta_Fmt"] = np.where(
      df_vis_det["Indicador"].isin(KPIS_PERCENTUAIS),
      df_vis_det["Meta"].map("{:.1f}%".format).str.replace(".", ","),
      df_vis_det["Meta"].map("{:.2f}".format).str.replace(".", ","),
  )
  df_vis_det["Real_Fmt"] = np.where(
      df_vis_det["Indicador"].isin(KPIS_PERCENTUAIS),
      df_vis_det["Real"].map("{:.1f}%".format).str.replace(".", ","),
      df_vis_det["Real"].map("{:.2f}".format).str.replace(".", ","),
  )

  st.dataframe(
      df_vis_det[[
          "Unidade",
          "GV",
          "Setor",
          "Indicador",
          "Base",
          "Meta_Fmt",
          "Real_Fmt",
          "%",
          "GAP",
          "MN",
          "Pontos",
      ]],
      column_config={
          "Meta_Fmt": "Meta",
          "Real_Fmt": "Real",
          "%": st.column_config.NumberColumn("% Atingimento", format="%.1f%%"),
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

# --- TAB 4: CONSOLIDADO POR RN (HTML/STYLING DE ALTA DENSIDADE E VISIBILIDADE) ---
with tab4:
  st.subheader("📌 Matriz Consolidada por RN")

  df_piv_base = df_detalhado_f.copy()

  # Formatação dos textos
  df_piv_base["Meta_Fmt"] = np.where(
      df_piv_base["Indicador"].isin(KPIS_PERCENTUAIS),
      df_piv_base["Meta"].map("{:.1f}%".format).str.replace(".", ","),
      df_piv_base["Meta"].map("{:.0f}".format),
  )
  df_piv_base["Real_Fmt"] = np.where(
      df_piv_base["Indicador"].isin(KPIS_PERCENTUAIS),
      df_piv_base["Real"].map("{:.1f}%".format).str.replace(".", ","),
      df_piv_base["Real"].map("{:.0f}".format),
  )
  df_piv_base["%_Fmt"] = (
      df_piv_base["%"].map("{:.1f}%".format).str.replace(".", ",")
  )
  df_piv_base["GAP_Fmt"] = np.where(
      df_piv_base["Indicador"].isin(KPIS_PERCENTUAIS),
      df_piv_base["GAP"].map("{:.1f}%".format).str.replace(".", ","),
      df_piv_base["GAP"].map("{:.2f}".format).str.replace(".", ","),
  )
  df_piv_base["MN_Fmt"] = df_piv_base["MN"].map("{:.2f}".format).str.replace(
      ".", ","
  )

  # Pivot para tabela
  df_pivot = df_piv_base.pivot(
      index=["Unidade", "Setor"],
      columns="Indicador",
      values=["Meta_Fmt", "Real_Fmt", "%_Fmt", "GAP_Fmt", "MN_Fmt"],
  )

  # Inverte níveis para colocar Nome do KPI no topo
  df_pivot = df_pivot.swaplevel(0, 1, axis=1)

  subcolunas_map = {
      "Meta_Fmt": "Meta",
      "Real_Fmt": "Real",
      "%_Fmt": "%",
      "GAP_Fmt": "GAP",
      "MN_Fmt": "MN",
  }
  df_pivot = df_pivot.rename(columns=subcolunas_map, level=1)

  kpis_presentes = [
      k for k in KPIS_OFICIAIS if k in df_pivot.columns.levels[0]
  ]
  ordem_subcolunas = ["Meta", "Real", "%", "GAP", "MN"]
  novas_colunas = pd.MultiIndex.from_product(
      [kpis_presentes, ordem_subcolunas], names=["Indicador", None]
  )
  df_pivot = df_pivot.reindex(columns=novas_colunas)


  # Função de Formatação Condicional para a coluna %
  def aplicar_cores_pivot(val):
    # Destaque verde para atingimento e tom pastel para o restante
    if isinstance(val, str) and "%" in val:
      try:
        num = float(
            val.replace("%", "").replace(",", ".").replace(" ", "").strip()
        )
        if num >= 100.0:
          return (
              "background-color: #c6f6d5; color: #22543d; font-weight: bold;"
          )
        elif num >= 95.0:
          return (
              "background-color: #feebc8; color: #744210; font-weight: bold;"
          )
        else:
          return "background-color: #fed7d7; color: #742a2a;"
      except:
        pass
    return ""


  # Aplicação do Styler do Pandas exportado em HTML puro para renderização perfeita
  styler = df_pivot.style.applymap(aplicar_cores_pivot)

  # Renderização da Tabela via HTML para controle absoluto de Font-Size e Cores no Print
  html_table = styler.to_html()
  html_table = html_table.replace('class="dataframe"', 'class="styled-table"')

  st.markdown(
      f'<div class="table-container-print">{html_table}</div>',
      unsafe_allow_html=True,
  )
