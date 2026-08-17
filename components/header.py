# ═══════════════════════════════════════════════════════════════════════════════
# COMPONENT: HEADER — Modern title bar with filter period badge
# ═══════════════════════════════════════════════════════════════════════════════

import textwrap
import streamlit as st
from config.tokens import COLORS, FONT_FAMILY, FONT_CDN
from config.icons import get_svg_icon


def render_header(period_label: str):
    """Renders the top application navigation/header bar."""
    icon_logo = get_svg_icon("logo", size=22, color=COLORS["orange"])
    icon_cal = get_svg_icon("calendar", size=14, color="#FFFFFF")

    html = textwrap.dedent(f"""
    <link href="{FONT_CDN}" rel="stylesheet">
    <div style="
        font-family: {FONT_FAMILY};
        padding: 16px 0 16px 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 2px solid {COLORS['orange']};
        margin-bottom: 24px;
    ">
        <div style="display: flex; align-items: center; gap: 14px;">
            <div style="
                width: 38px;
                height: 38px;
                background: {COLORS['green_dark']};
                border-radius: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 4px 12px rgba(27, 58, 45, 0.15);
            ">
                {icon_logo}
            </div>
            <div>
                <div style="
                    font-size: 1.45rem;
                    font-weight: 800;
                    color: {COLORS['text_primary']};
                    letter-spacing: -0.02em;
                    line-height: 1.1;
                ">
                    GESTÃO DE OFICINAS
                    <span style="font-size: 0.95rem; font-weight: 400; color: {COLORS['text_secondary']}; margin-left: 8px;">
                        | Atendimento das Reposições
                    </span>
                </div>
            </div>
        </div>
        <div>
            <div style="
                background: {COLORS['orange']};
                color: white;
                padding: 6px 16px;
                border-radius: 20px;
                font-size: 0.82rem;
                font-weight: 600;
                letter-spacing: 0.03em;
                display: inline-flex;
                align-items: center;
                gap: 8px;
                box-shadow: 0 2px 10px rgba(232, 118, 45, 0.25);
            ">
                {icon_cal}
                <span>{period_label}</span>
            </div>
        </div>
    </div>
    """)
    st.html(html)
