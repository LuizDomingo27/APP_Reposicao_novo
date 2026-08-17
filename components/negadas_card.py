# ═══════════════════════════════════════════════════════════════════════════════
# COMPONENT: NEGADAS CARD — Summary of denied requests and average volume
# ═══════════════════════════════════════════════════════════════════════════════

import textwrap
import streamlit as st
from config.tokens import COLORS, FONT_FAMILY, FONT_CDN
from config.icons import get_svg_icon


def render_negadas_card(total_negadas: int, media_pecas: float, total_pecas: int = 0):
    """Renders the Rejections card with standardized dark green gradient matching KPI cards."""
    icon_alert = get_svg_icon("alert_circle", size=20, color=COLORS["orange"])

    html = textwrap.dedent(f"""
    <link href="{FONT_CDN}" rel="stylesheet">
    <div style="
        font-family: {FONT_FAMILY};
        background: linear-gradient(135deg, {COLORS['green_dark']} 0%, {COLORS['green_mid']} 100%);
        border-radius: 16px;
        padding: 22px 28px;
        color: white;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 8px 30px rgba(27, 58, 45, 0.16);
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.08);
    ">
        <div style="
            position: absolute;
            top: -20px; right: 60px;
            width: 90px; height: 90px;
            background: rgba(232, 118, 45, 0.1);
            border-radius: 50%;
            pointer-events: none;
        "></div>
        <div>
            <div style="
                font-size: 0.72rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.12em;
                color: rgba(255, 255, 255, 0.7);
                margin-bottom: 6px;
                display: flex;
                align-items: center;
                gap: 8px;
            ">
                {icon_alert}
                <span>Reposições Negadas</span>
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
            ">solicitações reprovadas / não atendidas</div>
        </div>
        <div style="
            display: flex;
            gap: 14px;
        ">
            <div style="
                text-align: center;
                background: rgba(0, 0, 0, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 12px;
                padding: 12px 20px;
                backdrop-filter: blur(8px);
            ">
                <div style="
                    font-size: 0.68rem;
                    font-weight: 700;
                    text-transform: uppercase;
                    letter-spacing: 0.08em;
                    color: rgba(255, 255, 255, 0.6);
                    margin-bottom: 2px;
                ">Total Peças</div>
                <div style="
                    font-size: 1.6rem;
                    font-weight: 800;
                    color: {COLORS['green_light']};
                    line-height: 1.1;
                ">{total_pecas:,}</div>
                <div style="
                    font-size: 0.68rem;
                    color: rgba(255, 255, 255, 0.45);
                ">peças negadas</div>
            </div>
            <div style="
                text-align: center;
                background: rgba(0, 0, 0, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 12px;
                padding: 12px 20px;
                backdrop-filter: blur(8px);
            ">
                <div style="
                    font-size: 0.68rem;
                    font-weight: 700;
                    text-transform: uppercase;
                    letter-spacing: 0.08em;
                    color: rgba(255, 255, 255, 0.6);
                    margin-bottom: 2px;
                ">Média / Recusa</div>
                <div style="
                    font-size: 1.6rem;
                    font-weight: 800;
                    color: {COLORS['orange_warm']};
                    line-height: 1.1;
                ">{media_pecas:.1f}</div>
                <div style="
                    font-size: 0.68rem;
                    color: rgba(255, 255, 255, 0.45);
                ">peças / ocorrência</div>
            </div>
        </div>
    </div>
    """)
    st.html(html)

