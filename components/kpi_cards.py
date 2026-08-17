# ═══════════════════════════════════════════════════════════════════════════════
# COMPONENT: KPI CARDS — Main metric summary cards
# ═══════════════════════════════════════════════════════════════════════════════

import textwrap
import streamlit as st
from config.tokens import COLORS, FONT_FAMILY, FONT_CDN
from config.icons import get_svg_icon


def render_kpi_cards(total_repo: int, top_oficina: str, top_oficina_count: int):
    """Renders the two primary gradient KPI cards for total requests and top workshop."""
    icon_activity = get_svg_icon("activity", size=20, color=COLORS["orange"])
    icon_factory = get_svg_icon("factory", size=20, color=COLORS["green_light"])

    pct_oficina = ((top_oficina_count / total_repo) * 100 if total_repo > 0 else 0)

    html = textwrap.dedent(f"""
    <link href="{FONT_CDN}" rel="stylesheet">
    <div style="
        font-family: {FONT_FAMILY};
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        margin-bottom: 20px;
    ">
        <!-- Total Reposições -->
        <div style="
            background: linear-gradient(135deg, {COLORS['green_dark']} 0%, {COLORS['green_mid']} 100%);
            border-radius: 16px;
            padding: 24px 28px;
            color: white;
            position: relative;
            overflow: hidden;
            box-shadow: 0 8px 30px rgba(27, 58, 45, 0.16);
            border: 1px solid rgba(255, 255, 255, 0.08);
        ">
            <div style="
                position: absolute;
                top: -20px; right: -20px;
                width: 100px; height: 100px;
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
                {icon_activity}
                <span>Total de Reposições</span>
            </div>
            <div style="
                font-size: 2.8rem;
                font-weight: 800;
                color: {COLORS['orange']};
                line-height: 1;
                margin-bottom: 4px;
                letter-spacing: -0.02em;
            ">{total_repo:,}</div>
            <div style="
                font-size: 0.78rem;
                color: rgba(255, 255, 255, 0.5);
                font-weight: 400;
            ">solicitações registradas no período</div>
        </div>

        <!-- Oficina Top -->
        <div style="
            background: linear-gradient(135deg, {COLORS['green_dark']} 0%, {COLORS['green_mid']} 100%);
            border-radius: 16px;
            padding: 24px 28px;
            color: white;
            position: relative;
            overflow: hidden;
            box-shadow: 0 8px 30px rgba(27, 58, 45, 0.16);
            border: 1px solid rgba(255, 255, 255, 0.08);
        ">
            <div style="
                position: absolute;
                top: -15px; right: -15px;
                width: 80px; height: 80px;
                background: rgba(93, 181, 91, 0.1);
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
                {icon_factory}
                <span>Oficina que Mais Solicita</span>
            </div>
            <div style="
                font-size: 1.25rem;
                font-weight: 700;
                color: white;
                line-height: 1.25;
                margin-bottom: 12px;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            ">{top_oficina}</div>
            <div style="
                display: inline-flex;
                align-items: center;
                background: rgba(232, 118, 45, 0.15);
                border: 1px solid rgba(232, 118, 45, 0.35);
                border-radius: 8px;
                padding: 4px 12px;
            ">
                <span style="
                    font-size: 1.1rem;
                    font-weight: 700;
                    color: {COLORS['orange']};
                ">{top_oficina_count}</span>
                <span style="
                    font-size: 0.75rem;
                    color: rgba(255, 255, 255, 0.6);
                    margin-left: 6px;
                ">reposições ({pct_oficina:.1f}%)</span>
            </div>
        </div>
    </div>
    """)
    st.html(html)
