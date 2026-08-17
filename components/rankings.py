# ═══════════════════════════════════════════════════════════════════════════════
# COMPONENT: RANKINGS — Top 3 Matéria-Prima & Top 3 Partes da Peça
# ═══════════════════════════════════════════════════════════════════════════════

import textwrap
from typing import List, Tuple
import streamlit as st
from config.tokens import COLORS, FONT_FAMILY, FONT_CDN
from config.icons import get_svg_icon


def _build_ranking_items(data: List[Tuple[str, int, float]], color: str) -> str:
    """Builds the progress-bar rows for a single ranking card."""
    if not data:
        return f"<div style='color: {COLORS['text_secondary']}; font-size: 0.85rem; padding: 12px 0;'>Nenhum dado disponível para o período.</div>"

    items_html = ""
    max_val = data[0][1] if data else 1
    for i, (name, count, pct) in enumerate(data[:3]):
        bar_width = (count / max_val) * 100 if max_val > 0 else 0
        rank_label = f"0{i+1}"

        if i == 0:
            badge_bg = COLORS['green_dark']
            badge_fg = "#FFFFFF"
        elif i == 1:
            badge_bg = COLORS['bg_secondary']
            badge_fg = COLORS['text_primary']
        else:
            badge_bg = "#F5F5F5"
            badge_fg = COLORS['text_secondary']

        items_html += f"""
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 14px;">
            <span style="font-size: 0.75rem; font-weight: 700; width: 26px; height: 26px; border-radius: 8px; background: {badge_bg}; color: {badge_fg}; display: inline-flex; align-items: center; justify-content: center; flex-shrink: 0; letter-spacing: -0.02em;">{rank_label}</span>
            <div style="flex: 1; min-width: 0;">
                <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 5px;">
                    <span style="font-size: 0.85rem; font-weight: 600; color: {COLORS['text_primary']}; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 65%;">{name}</span>
                    <span style="font-size: 0.78rem; font-weight: 600; color: {COLORS['text_secondary']};">{count:,} <span style="font-weight: 400; font-size: 0.72rem;">({pct:.1f}%)</span></span>
                </div>
                <div style="width: 100%; height: 6px; background: {COLORS['bar_track']}; border-radius: 3px; overflow: hidden;">
                    <div style="width: {bar_width}%; height: 100%; background: linear-gradient(90deg, {color} 0%, {color}CC 100%); border-radius: 3px;"></div>
                </div>
            </div>
        </div>
        """
    return items_html


def render_ranking_card(
    title: str,
    data: List[Tuple[str, int, float]],
    bar_color: str,
    icon_name: str,
    accent_color: str,
):
    """Renders a single Top 3 ranking card (fits inside a column)."""
    items = _build_ranking_items(data, bar_color)
    icon = get_svg_icon(icon_name, size=16, color=accent_color)

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
        height: 100%;
    ">
        <div style="
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: {COLORS['text_primary']};
            margin-bottom: 16px;
            padding-bottom: 10px;
            border-bottom: 2px solid {accent_color};
            display: flex;
            align-items: center;
            gap: 8px;
        ">
            {icon}
            <span>{title}</span>
        </div>
        {items}
    </div>
    """)
    st.html(html)
