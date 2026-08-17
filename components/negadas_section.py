# ═══════════════════════════════════════════════════════════════════════════════
# COMPONENT: NEGADAS SECTION — Dedicated Section for Denied/Rejected Requests
# Standardized dark green gradient KPI cards + 2 Bar charts with top value labels
# ═══════════════════════════════════════════════════════════════════════════════

import textwrap
from typing import Dict, Any
import streamlit as st
from config.tokens import COLORS, FONT_FAMILY, FONT_CDN
from config.icons import get_svg_icon
from components.charts import build_bar_chart_html


def render_negadas_section(
    negadas_metrics: Dict[str, Any],
    negadas_distribution: Dict[str, Any],
):
    """
    Renders the dedicated section for denied/rejected requests with:
    - Standardized KPI cards matching the Total Reposições layout
    - 2 analytical column charts (Count of Denials and Sum of Pieces) with top value labels
    """
    total_negadas = negadas_metrics.get("total_negadas", 0)
    total_pecas = negadas_metrics.get("total_pecas", 0)
    media_pecas = negadas_metrics.get("media_pecas", 0.0)

    icon_alert = get_svg_icon("alert_circle", size=20, color=COLORS["orange"])
    icon_package = get_svg_icon("package", size=20, color=COLORS["green_light"])
    icon_activity = get_svg_icon("activity", size=20, color=COLORS["orange_warm"])

    # Section Header HTML
    section_header_html = textwrap.dedent(f"""
    <link href="{FONT_CDN}" rel="stylesheet">
    <div style="
        font-family: {FONT_FAMILY};
        margin-top: 36px;
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 2px solid {COLORS['orange']};
        display: flex;
        align-items: center;
        justify-content: space-between;
    ">
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="
                width: 32px;
                height: 32px;
                background: {COLORS['green_dark']};
                border-radius: 8px;
                display: flex;
                align-items: center;
                justify-content: center;
            ">
                {icon_alert}
            </div>
            <div>
                <div style="
                    font-size: 1.25rem;
                    font-weight: 800;
                    color: {COLORS['text_primary']};
                    letter-spacing: -0.01em;
                    line-height: 1.1;
                ">
                    AUDITORIA DE REPOSIÇÕES NEGADAS
                </div>
                <div style="
                    font-size: 0.76rem;
                    color: {COLORS['text_secondary']};
                    font-weight: 500;
                ">
                    Análise detalhada de ocorrências recusadas e impacto volumétrico de peças
                </div>
            </div>
        </div>
        <div style="
            background: rgba(232, 118, 45, 0.12);
            border: 1px solid rgba(232, 118, 45, 0.25);
            color: {COLORS['orange']};
            padding: 4px 14px;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        ">
            Recusas & Não Atendimentos
        </div>
    </div>
    """)
    st.html(section_header_html)

    # 3 Standardized KPI Cards (matching Total Reposições layout)
    kpis_html = textwrap.dedent(f"""
    <link href="{FONT_CDN}" rel="stylesheet">
    <div style="
        font-family: {FONT_FAMILY};
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 20px;
        margin-bottom: 24px;
    ">
        <!-- Card 1: Total de Solicitações Negadas -->
        <div style="
            background: linear-gradient(135deg, {COLORS['green_dark']} 0%, {COLORS['green_mid']} 100%);
            border-radius: 16px;
            padding: 22px 26px;
            color: white;
            position: relative;
            overflow: hidden;
            box-shadow: 0 8px 30px rgba(27, 58, 45, 0.16);
            border: 1px solid rgba(255, 255, 255, 0.08);
        ">
            <div style="
                position: absolute;
                top: -20px; right: -20px;
                width: 90px; height: 90px;
                background: rgba(232, 118, 45, 0.12);
                border-radius: 50%;
                pointer-events: none;
            "></div>
            <div style="
                display: flex;
                align-items: center;
                gap: 8px;
                font-size: 0.72rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.12em;
                color: rgba(255, 255, 255, 0.7);
                margin-bottom: 8px;
            ">
                {icon_alert}
                <span>Total de Solicitações Negadas</span>
            </div>
            <div style="
                font-size: 2.6rem;
                font-weight: 800;
                color: {COLORS['orange']};
                line-height: 1;
                margin-bottom: 4px;
                letter-spacing: -0.02em;
            ">{total_negadas:,}</div>
            <div style="
                font-size: 0.78rem;
                color: rgba(255, 255, 255, 0.5);
                font-weight: 400;
            ">ocorrências recusadas no período</div>
        </div>

        <!-- Card 2: Total de Peças Negadas -->
        <div style="
            background: linear-gradient(135deg, {COLORS['green_dark']} 0%, {COLORS['green_mid']} 100%);
            border-radius: 16px;
            padding: 22px 26px;
            color: white;
            position: relative;
            overflow: hidden;
            box-shadow: 0 8px 30px rgba(27, 58, 45, 0.16);
            border: 1px solid rgba(255, 255, 255, 0.08);
        ">
            <div style="
                position: absolute;
                top: -15px; right: -15px;
                width: 85px; height: 85px;
                background: rgba(93, 181, 91, 0.12);
                border-radius: 50%;
                pointer-events: none;
            "></div>
            <div style="
                display: flex;
                align-items: center;
                gap: 8px;
                font-size: 0.72rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.12em;
                color: rgba(255, 255, 255, 0.7);
                margin-bottom: 8px;
            ">
                {icon_package}
                <span>Total de Peças Negadas</span>
            </div>
            <div style="
                font-size: 2.6rem;
                font-weight: 800;
                color: {COLORS['green_light']};
                line-height: 1;
                margin-bottom: 4px;
                letter-spacing: -0.02em;
            ">{total_pecas:,}</div>
            <div style="
                font-size: 0.78rem;
                color: rgba(255, 255, 255, 0.5);
                font-weight: 400;
            ">volume total de peças não repostas</div>
        </div>

        <!-- Card 3: Média de Peças por Solicitação -->
        <div style="
            background: linear-gradient(135deg, {COLORS['green_dark']} 0%, {COLORS['green_mid']} 100%);
            border-radius: 16px;
            padding: 22px 26px;
            color: white;
            position: relative;
            overflow: hidden;
            box-shadow: 0 8px 30px rgba(27, 58, 45, 0.16);
            border: 1px solid rgba(255, 255, 255, 0.08);
        ">
            <div style="
                position: absolute;
                top: -15px; right: -15px;
                width: 85px; height: 85px;
                background: rgba(255, 183, 77, 0.12);
                border-radius: 50%;
                pointer-events: none;
            "></div>
            <div style="
                display: flex;
                align-items: center;
                gap: 8px;
                font-size: 0.72rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.12em;
                color: rgba(255, 255, 255, 0.7);
                margin-bottom: 8px;
            ">
                {icon_activity}
                <span>Média por Solicitação</span>
            </div>
            <div style="
                font-size: 2.6rem;
                font-weight: 800;
                color: {COLORS['orange_warm']};
                line-height: 1;
                margin-bottom: 4px;
                letter-spacing: -0.02em;
            ">{media_pecas:.1f}</div>
            <div style="
                font-size: 0.78rem;
                color: rgba(255, 255, 255, 0.5);
                font-weight: 400;
            ">peças / ocorrência de recusa</div>
        </div>
    </div>
    """)
    st.html(kpis_html)

    # 2 Bar Charts (Distribution of Denied Requests & Sum of Pieces Denied)
    chart_col1, chart_col2 = st.columns([1, 1], gap="medium")

    weekly_labels = negadas_distribution.get("weekly_negadas_labels", [])
    weekly_negadas_vals = negadas_distribution.get("weekly_negadas_values", [])
    weekly_pecas_vals = negadas_distribution.get("weekly_pecas_values", [])

    # If weekly is empty, fallback to monthly
    if not weekly_labels:
        weekly_labels = negadas_distribution.get("monthly_negadas_labels", [])
        weekly_negadas_vals = negadas_distribution.get("monthly_negadas_values", [])
        weekly_pecas_vals = negadas_distribution.get("monthly_pecas_values", [])

    with chart_col1:
        negadas_bar_html = build_bar_chart_html(
            labels=weekly_labels,
            values=weekly_negadas_vals,
            title="Distribuição de Solicitações Negadas (por Período)",
            icon_name="alert_circle",
            color_start=COLORS["orange"],
            color_end=COLORS["orange_warm"],
            border_accent_color=COLORS["orange"],
            chart_id="negadasCountChart",
            height=340,
            dataset_label="Solicitações Negadas"
        )
        st.components.v1.html(negadas_bar_html, height=440, scrolling=False)

    with chart_col2:
        pecas_bar_html = build_bar_chart_html(
            labels=weekly_labels,
            values=weekly_pecas_vals,
            title="Volume de Peças Negadas (por Período)",
            icon_name="package",
            color_start=COLORS["green_light"],
            color_end=COLORS["green_accent"],
            border_accent_color=COLORS["green_light"],
            chart_id="negadasPecasChart",
            height=340,
            dataset_label="Peças Negadas"
        )
        st.components.v1.html(pecas_bar_html, height=440, scrolling=False)
