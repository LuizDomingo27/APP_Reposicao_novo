# ═══════════════════════════════════════════════════════════════════════════════
# COMPONENT: KPI CARDS — Chamados summary cards (light tinted reference style)
# ═══════════════════════════════════════════════════════════════════════════════

import textwrap
from typing import Any, Dict
import streamlit as st
from config.tokens import COLORS, CARD_TINTS, FONT_FAMILY, FONT_CDN
from config.icons import get_svg_icon


# ── pt-BR number formatting helpers ─────────────────────────────────────────────

def _fmt_int(n: int) -> str:
    return f"{int(n):,}".replace(",", ".")


def _fmt_pct(x: float) -> str:
    return f"{x:.2f}".replace(".", ",") + "%"


def _fmt_dec(x: float, decimals: int = 2) -> str:
    s = f"{x:,.{decimals}f}"          # e.g. '1,234.56'
    return s.replace(",", "§").replace(".", ",").replace("§", ".")


def _card(tint_name: str, icon_name: str, label: str, value: str, subtitle: str) -> str:
    """Builds a single light, tinted KPI card matching the reference dashboard."""
    tint = CARD_TINTS[tint_name]
    icon = get_svg_icon(icon_name, size=20, color=tint["fg"])
    return f"""
        <div style="
            background: {tint['bg']};
            border: 1px solid {tint['border']};
            border-radius: 14px;
            padding: 18px 20px;
            box-shadow: 0 1px 3px rgba(27,58,45,0.04);
        ">
            <div style="display:flex; align-items:flex-start; justify-content:space-between; gap:12px;">
                <div style="
                    font-size: 0.82rem;
                    font-weight: 600;
                    color: {COLORS['text_secondary']};
                    line-height: 1.25;
                ">{label}</div>
                <div style="
                    width: 38px; height: 38px;
                    flex-shrink: 0;
                    background: {tint['icon_bg']};
                    border-radius: 10px;
                    display: flex; align-items: center; justify-content: center;
                ">{icon}</div>
            </div>
            <div style="
                font-size: 1.9rem;
                font-weight: 800;
                color: {COLORS['text_primary']};
                line-height: 1.1;
                margin-top: 10px;
                letter-spacing: -0.02em;
            ">{value}</div>
            <div style="
                font-size: 0.76rem;
                color: {COLORS['text_muted']};
                font-weight: 500;
                margin-top: 4px;
                min-height: 1em;
            ">{subtitle}</div>
        </div>
    """


def _text_card(tint_name: str, icon_name: str, label: str, value: str, subtitle: str) -> str:
    """Builds a highlight card whose value is (potentially long) text, not a number."""
    tint = CARD_TINTS[tint_name]
    icon = get_svg_icon(icon_name, size=20, color=tint["fg"])
    return f"""
        <div style="
            background: {tint['bg']};
            border: 1px solid {tint['border']};
            border-radius: 14px;
            padding: 18px 20px;
            box-shadow: 0 1px 3px rgba(27,58,45,0.04);
        ">
            <div style="display:flex; align-items:flex-start; justify-content:space-between; gap:12px;">
                <div style="font-size: 0.82rem; font-weight: 600; color: {COLORS['text_secondary']}; line-height: 1.25;">{label}</div>
                <div style="
                    width: 38px; height: 38px; flex-shrink: 0;
                    background: {tint['icon_bg']};
                    border-radius: 10px;
                    display: flex; align-items: center; justify-content: center;
                ">{icon}</div>
            </div>
            <div style="
                font-size: 1.12rem;
                font-weight: 800;
                color: {COLORS['text_primary']};
                line-height: 1.25;
                margin-top: 10px;
                letter-spacing: -0.01em;
                display: -webkit-box;
                -webkit-line-clamp: 2;
                -webkit-box-orient: vertical;
                overflow: hidden;
            " title="{value}">{value}</div>
            <div style="
                font-size: 0.76rem;
                color: {COLORS['text_muted']};
                font-weight: 500;
                margin-top: 4px;
                min-height: 1em;
            ">{subtitle}</div>
        </div>
    """


def render_highlight_cards(highlights: Dict[str, Any]):
    """Renders the two highlight cards: top workshop and top reposição motive."""
    oficina = highlights.get("top_oficina", "N/A")
    oficina_count = highlights.get("top_oficina_count", 0)
    motivo = highlights.get("top_motivo", "N/A")
    motivo_count = highlights.get("top_motivo_count", 0)

    cards = [
        _text_card("slate", "factory", "Oficina que Mais Solicita",
                   oficina, f"{_fmt_int(oficina_count)} reposições no período"),
        _text_card("amber", "alert_circle", "Principal Motivo",
                   motivo, f"{_fmt_int(motivo_count)} ocorrências"),
    ]

    html = textwrap.dedent(f"""
    <link href="{FONT_CDN}" rel="stylesheet">
    <div style="
        font-family: {FONT_FAMILY};
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 16px;
        margin-bottom: 22px;
    ">
        {''.join(cards)}
    </div>
    """)
    st.html(html)


def render_kpi_cards(kpis: Dict[str, Any]):
    """Renders the responsive grid of Chamados KPI cards."""
    total = kpis.get("total_chamados", 0)
    finalizados = kpis.get("finalizados", 0)
    em_andamento = kpis.get("em_andamento", 0)
    taxa = kpis.get("taxa_finalizacao", 0.0)
    total_pecas = kpis.get("total_pecas", 0)
    media_pecas = kpis.get("media_pecas", 0.0)

    cards = [
        _card("blue", "clipboard", "Total de Chamados",
              _fmt_int(total), "chamados no período"),
        _card("green", "check_circle", "Taxa de Finalização",
              _fmt_pct(taxa), f"{_fmt_int(finalizados)} finalizados"),
        _card("amber", "clock", "Em Andamento",
              _fmt_int(em_andamento), "chamados abertos"),
        _card("indigo", "package", "Total Peças Solicitadas",
              _fmt_int(total_pecas), "peças solicitadas"),
    ]

    html = textwrap.dedent(f"""
    <link href="{FONT_CDN}" rel="stylesheet">
    <div style="
        font-family: {FONT_FAMILY};
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 16px;
        margin-bottom: 22px;
    ">
        {''.join(cards)}
    </div>
    """)
    st.html(html)
