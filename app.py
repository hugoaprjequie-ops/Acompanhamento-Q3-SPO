import numpy as np
import pandas as pd
from PIL import Image
import streamlit as st

st.set_page_config(
    page_title="Acompanhamento GP7 - Ranking & Indicadores",
    page_icon="🏆",
    layout="wide",
)

try:
  image = Image.open("4d040808-a146-4bd0-b079-9d95b6195549.jpg")
  st.image(image, use_container_width=True)
except Exception:
  st.image(
      "https://raw.githubusercontent.com/hugoaprjequie-ops/Acompanhamento-Q3-SPO/main/4d040808-a146-4bd0-b079-9d95b6195549.jpg",
      use_container_width=True,
  )

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
    @media print {
        body * { visibility: hidden; }
        #print-area, #print-area * { visibility: visible; }
        #print-area { position: absolute; left: 0; top: 0; width: 100%; }
    }
</style>
""",
    unsafe_allow_html=True,
)


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

# --- FILTROS ---
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

# --- CABEÇALHO ---
st.title("🏆 Painel de Gamificação e Performance GP7")
st.caption(
    "Acompanhamento diário de Metas, Atingimentos, Pontuação e Ranking dos RNs"
)

# --- CARDS RESUMO ---
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

st.markdown("---")

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
                <h3>🥇 1º Lugar</h3>
                <h4>Setor {top3.iloc[0]['Setor']} ({top3.iloc[0]['GV']})</h4>
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
                <h4>Setor {top3.iloc[1]['Setor']} ({top3.iloc[1]['GV']})</h4>
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
                <h4>Setor {top3.iloc[2]['Setor']} ({top3.iloc[2]['GV']})</h4>
                <p><b>{top3.iloc[2]['Pontos_Acumulados']} Pts</b> ({top3.iloc[2]['%_Atingimento_Pontos']:.1f}%)</p>
                <p>{top3.iloc[2]['Selo']}</p>
            </div>
            """,
          unsafe_allow_html=True,
      )

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

# --- TAB 4: CONSOLIDADO POR RN (AGRUPADO POR KPI NO TOPO: META | REAL | % | GAP | MN) ---
with tab4:
  st.subheader("📌 Matriz Consolidada por RN")

  col_btn1, col_btn2 = st.columns([1, 4])
  with col_btn1:
    st.markdown(
        """
        <button onclick="window.print()" style="
            background-color: #28a745;
            color: white;
            border: none;
            padding: 8px 16px;
            font-size: 14px;
            font-weight: bold;
            border-radius: 5px;
            cursor: pointer;">
            🖨️ Imprimir / Salvar PDF
        </button>
        """,
        unsafe_allow_html=True,
    )

  st.markdown('<div id="print-area">', unsafe_allow_html=True)

  df_piv_base = df_detalhado_f.copy()

  # Formatação dos campos
  df_piv_base["Meta"] = np.where(
      df_piv_base["Indicador"].isin(KPIS_PERCENTUAIS),
      df_piv_base["Meta"].map("{:.1f}%".format).str.replace(".", ","),
      df_piv_base["Meta"].map("{:.0f}".format),
  )
  df_piv_base["Real"] = np.where(
      df_piv_base["Indicador"].isin(KPIS_PERCENTUAIS),
      df_piv_base["Real"].map("{:.1f}%".format).str.replace(".", ","),
      df_piv_base["Real"].map("{:.0f}".format),
  )
  df_piv_base["%"] = df_piv_base["%"].map("{:.1f}%".format).str.replace(".", ",")
  df_piv_base["GAP"] = np.where(
      df_piv_base["Indicador"].isin(KPIS_PERCENTUAIS),
      df_piv_base["GAP"].map("{:.1f}%".format).str.replace(".", ","),
      df_piv_base["GAP"].map("{:.2f}".format).str.replace(".", ","),
  )
  df_piv_base["MN"] = df_piv_base["MN"].map("{:.2f}".format).str.replace(
      ".", ","
  )

  # 1. Pivot inicial
  df_pivot = df_piv_base.pivot(
      index=["Unidade", "Setor"],
      columns="Indicador",
      values=["Meta", "Real", "%", "GAP", "MN"],
  )

  # 2. Inverte para colocar Indicador no Nível 0 (Topo) e Métricas no Nível 1 (Baixo)
  df_pivot = df_pivot.swaplevel(0, 1, axis=1)

  # 3. Constroi a ordem de colunas exata para cada KPI ter Meta -> Real -> % -> GAP -> MN
  kpis_presentes = [
      k for k in KPIS_OFICIAIS if k in df_pivot.columns.levels[0]
  ]
  subcolunas = ["Meta", "Real", "%", "GAP", "MN"]
  novas_colunas = pd.MultiIndex.from_product(
      [kpis_presentes, subcolunas], names=["Indicador", None]
  )

  # 4. Aplica a reindexação estruturada
  df_pivot = df_pivot.reindex(columns=novas_colunas)

  st.dataframe(df_pivot, use_container_width=True)

  st.markdown("</div>", unsafe_allow_html=True)
