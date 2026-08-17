# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ORCHESTRATOR — Application Entry Point & Layer Coordination
# ═══════════════════════════════════════════════════════════════════════════════

import textwrap
from datetime import datetime
import streamlit as st

# Layer Imports
from config.tokens import COLORS, FONT_CDN, FONT_FAMILY
from data.loader import load_data, DataLoadError
from data.filters import filter_by_date_range, get_date_range_label
from data.metrics import (
    get_chamados_kpis,
    get_highlights,
    get_status_distribution,
    get_rankings,
    get_monthly_history,
    get_weekly_distribution,
)
from components.navbar import render_navbar
from components.header import render_header
from components.kpi_cards import render_kpi_cards, render_highlight_cards
from components.rankings import render_ranking_card
from components.monthly_table import render_monthly_table
from components.charts import build_donut_chart_html, build_area_chart_html
from components.welcome import render_welcome

# ─── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Gestão de Reposições | Dashboard Corporativo",
    page_icon=":material/analytics:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Global Styling & Resets ──────────────────────────────────────────────────
global_css = textwrap.dedent(f"""
<link href="{FONT_CDN}" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet">
<style>
    *, *::before, *::after {{ box-sizing: border-box; }}

    html, body, .main, p, h1, h2, h3, h4, h5, h6, label {{
        font-family: {FONT_FAMILY} !important;
    }}

    /* Protect Streamlit Material Symbols / Icon fonts */
    .material-symbols-rounded,
    .material-symbols-outlined,
    [data-testid*="stIcon"],
    [data-testid="stIconMaterial"] {{
        font-family: 'Material Symbols Rounded', 'Material Symbols Outlined' !important;
        font-style: normal !important;
    }}

    /* Hide Streamlit default chrome & sidebar entirely */
    header[data-testid="stHeader"],
    [data-testid="stSidebar"],
    [data-testid="stSidebarCollapsedControl"],
    #MainMenu, footer, .stDeployButton {{
        display: none !important;
    }}

    /* Main container styling */
    .main {{
        background-color: {COLORS['bg_primary']};
    }}
    .main .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
        max-width: 1520px;
    }}

    /* Form Controls & Inputs (Navbar area) */
    .stSelectbox label,
    .stDateInput label,
    .stFileUploader label {{
        color: {COLORS['text_primary']} !important;
        font-weight: 700 !important;
        font-size: 0.78rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 4px !important;
    }}

    [data-baseweb="select"] *,
    [data-baseweb="input"] *,
    input {{
        color: {COLORS['text_primary']} !important;
        font-weight: 600 !important;
        font-family: {FONT_FAMILY} !important;
    }}
    [data-baseweb="select"] {{
        background-color: #FFFFFF !important;
        border-radius: 10px !important;
        border: 1px solid {COLORS['border_card']} !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.03) !important;
    }}
    [data-baseweb="input"] {{
        background-color: #FFFFFF !important;
        border-radius: 10px !important;
        border: 1px solid {COLORS['border_card']} !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.03) !important;
    }}

    /* Compact File Uploader */
    [data-testid="stFileUploader"] {{
        background: transparent !important;
    }}
    [data-testid="stFileUploaderDropzone"] {{
        background: #FFFFFF !important;
        border: 1.5px dashed {COLORS['orange']} !important;
        border-radius: 10px !important;
        padding: 6px 12px !important;
        min-height: 42px !important;
    }}
    [data-testid="stFileUploaderDropzone"]:hover {{
        background: {COLORS['bg_secondary']} !important;
    }}
    [data-testid="stFileUploaderDropzone"] button {{
        background: {COLORS['orange']} !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 4px 12px !important;
        font-size: 0.8rem !important;
    }}

    /* Clean iframe container */
    iframe {{
        border: none !important;
        width: 100% !important;
        overflow: hidden !important;
    }}

    /* Custom Streamlit Alert / Warning overrides */
    [data-testid="stAlert"] {{
        border-radius: 12px !important;
        border: 1px solid {COLORS['border_card']} !important;
        background-color: {COLORS['bg_card']} !important;
        color: {COLORS['text_primary']} !important;
        font-weight: 500 !important;
    }}

    /* Spacing fixes */
    div[data-testid="stVerticalBlock"] > div {{
        gap: 1.25rem !important;
    }}
</style>
""")
st.html(global_css)


def main():
    """Main application loop."""
    # 1. Top Navbar (Branding, Dataset Upload & Date Filters)
    uploaded_file, start_date, end_date, period_type = render_navbar()

    if uploaded_file is None:
        # Initial empty state view
        render_welcome()
        return

    # 2. Data Ingestion Layer
    try:
        df_repo = load_data(uploaded_file)
    except DataLoadError as e:
        st.error(f"Não foi possível processar a planilha enviada: {e}")
        return
    except Exception as e:
        st.error(f"Ocorreu um erro inesperado ao ler os dados: {e}")
        return

    # 3. Filtering Layer
    df_filtered = filter_by_date_range(df_repo, "DATA", start_date, end_date)
    period_label = get_date_range_label(start_date, end_date)

    # 4. Presentation Header
    render_header(period_label)

    if df_filtered.empty:
        st.info("Nenhum dado encontrado para o período selecionado. Ajuste o intervalo de datas no menu acima.")
        return

    # 5. Business Metrics Layer — Chamados
    kpis = get_chamados_kpis(df_filtered)
    highlights = get_highlights(df_filtered)
    status_dist = get_status_distribution(df_filtered)
    rankings = get_rankings(df_filtered, top_n=3)

    # 6. Presentation Layer: KPI Cards + Highlights
    render_kpi_cards(kpis)
    render_highlight_cards(highlights)

    # 7. Presentation Layer: Weekly Evolution + Status + 3-Month Proportion
    weekly_data = get_weekly_distribution(df_filtered, max_weeks=13)
    monthly_data = get_monthly_history(df_repo, n_months=3)

    col_area, col_status, col_prop = st.columns([1.6, 1, 1], gap="medium")

    with col_area:
        area_html = build_area_chart_html(
            labels=weekly_data["labels"],
            values=weekly_data["values"],
            title="Chamados por Semana",
            subtitle="Evolução semanal do volume de chamados",
            chart_id="chamadosWeeklyChart",
            height=340,
            dataset_label="Chamados",
        )
        st.components.v1.html(area_html, height=470, scrolling=False)

    with col_status:
        status_html = build_donut_chart_html(
            labels=status_dist["labels"],
            values=status_dist["values"],
            colors=status_dist["colors"] or None,
            title="Status dos Chamados",
            center_label="Total",
        )
        st.components.v1.html(status_html, height=470, scrolling=False)

    with col_prop:
        prop_html = build_donut_chart_html(
            labels=monthly_data["labels"],
            values=monthly_data["values"],
            title="Proporção - Últimos 3 Meses",
            center_label="Total Geral",
        )
        st.components.v1.html(prop_html, height=470, scrolling=False)

    # 8. Presentation Layer: Supporting Rankings & Monthly History (single row)
    rank_col1, rank_col2, rank_col3 = st.columns(3, gap="medium")

    with rank_col1:
        render_ranking_card(
            title="Top 3 Linhas de Matéria-Prima",
            data=rankings["mp_data"],
            bar_color=COLORS["green_light"],
            icon_name="layers",
            accent_color=COLORS["green_accent"],
        )

    with rank_col2:
        render_ranking_card(
            title="Top 3 Partes da Peça Solicitadas",
            data=rankings["parte_data"],
            bar_color=COLORS["orange"],
            icon_name="package",
            accent_color=COLORS["orange"],
        )

    with rank_col3:
        render_monthly_table(monthly_data["table_data"])


if __name__ == "__main__":
    main()

