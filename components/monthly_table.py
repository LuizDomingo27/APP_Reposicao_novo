# ═══════════════════════════════════════════════════════════════════════════════
# COMPONENT: MONTHLY TABLE — Tabular breakdown of historical monthly totals
# ═══════════════════════════════════════════════════════════════════════════════

import textwrap
from typing import List, Tuple
import streamlit as st
from config.tokens import COLORS, FONT_FAMILY, FONT_CDN
from config.icons import get_svg_icon


def render_monthly_table(month_data: List[Tuple[str, int]]):
    """Renders the monthly comparison table without emojis."""
    icon_table = get_svg_icon("table", size=16, color=COLORS["green_dark"])

    rows_html = ""
    for month_label, total in month_data:
        rows_html += f"""
        <tr>
            <td style="padding: 10px 14px; font-size: 0.85rem; font-weight: 500; color: {COLORS['text_primary']}; border-bottom: 1px solid {COLORS['border_card']};">{month_label}</td>
            <td style="padding: 10px 14px; font-size: 0.9rem; font-weight: 700; color: {COLORS['text_primary']}; text-align: right; border-bottom: 1px solid {COLORS['border_card']};">{total:,}</td>
        </tr>
        """

    html = textwrap.dedent(f"""
    <link href="{FONT_CDN}" rel="stylesheet">
    <div style="
        font-family: {FONT_FAMILY};
        background: {COLORS['bg_card']};
        border-radius: 16px;
        padding: 22px 26px;
        border: 1px solid {COLORS['border_card']};
        box-shadow: 0 2px 12px rgba(0,0,0,0.03);
        margin-bottom: 20px;
    ">
        <div style="
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: {COLORS['text_primary']};
            margin-bottom: 14px;
            padding-bottom: 10px;
            border-bottom: 2px solid {COLORS['green_dark']};
            display: flex;
            align-items: center;
            gap: 8px;
        ">
            {icon_table}
            <span>Histórico Mensal Consolidado</span>
        </div>
        <table style="width: 100%; border-collapse: collapse;">
            <thead>
                <tr>
                    <th style="padding: 6px 14px 10px 14px; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: {COLORS['text_secondary']}; text-align: left; border-bottom: 1px solid {COLORS['border_card']};">Mês / Ano</th>
                    <th style="padding: 6px 14px 10px 14px; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: {COLORS['text_secondary']}; text-align: right; border-bottom: 1px solid {COLORS['border_card']};">Reposições</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </div>
    """)
    st.html(html)
