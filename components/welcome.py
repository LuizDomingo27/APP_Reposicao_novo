# ═══════════════════════════════════════════════════════════════════════════════
# COMPONENT: WELCOME — Empty state hero view prompting file upload
# ═══════════════════════════════════════════════════════════════════════════════

import textwrap
import streamlit as st
from config.tokens import COLORS, FONT_FAMILY, FONT_CDN
from config.icons import get_svg_icon


def render_welcome():
    """Renders a sleek, modern landing screen when no file is uploaded."""
    icon_logo = get_svg_icon("logo", size=48, color=COLORS["orange"])
    icon_upload = get_svg_icon("upload", size=20, color="#FFFFFF")
    icon_table = get_svg_icon("file_spreadsheet", size=18, color=COLORS["green_light"])

    html = textwrap.dedent(f"""
    <link href="{FONT_CDN}" rel="stylesheet">
    <div style="
        font-family: {FONT_FAMILY};
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 72vh;
        text-align: center;
        padding: 40px 20px;
    ">
        <div style="
            width: 88px;
            height: 88px;
            background: linear-gradient(135deg, {COLORS['green_dark']} 0%, {COLORS['green_mid']} 100%);
            border-radius: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 24px;
            box-shadow: 0 12px 36px rgba(27, 58, 45, 0.25);
            border: 1px solid rgba(255, 255, 255, 0.1);
        ">
            {icon_logo}
        </div>
        
        <div style="
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(232, 118, 45, 0.12);
            border: 1px solid rgba(232, 118, 45, 0.25);
            padding: 4px 14px;
            border-radius: 20px;
            color: {COLORS['orange']};
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 16px;
        ">
            {icon_table}
            <span>Painel de Inteligência Operacional</span>
        </div>

        <h1 style="
            font-size: 2.5rem;
            font-weight: 800;
            color: {COLORS['text_primary']};
            margin-bottom: 12px;
            letter-spacing: -0.03em;
            line-height: 1.15;
        ">
            Gestão de Reposições
        </h1>
        
        <p style="
            font-size: 1.05rem;
            color: {COLORS['text_secondary']};
            font-weight: 400;
            max-width: 480px;
            line-height: 1.6;
            margin-bottom: 36px;
        ">
            Monitore a volumetria, indicadores por oficina, matérias-primas críticas e motivos de recusa em tempo real.
        </p>

        <div style="
            background: linear-gradient(135deg, {COLORS['green_dark']} 0%, {COLORS['green_mid']} 100%);
            border-radius: 14px;
            padding: 16px 28px;
            color: white;
            display: inline-flex;
            align-items: center;
            gap: 12px;
            box-shadow: 0 8px 24px rgba(27, 58, 45, 0.2);
            font-size: 0.95rem;
            font-weight: 500;
        ">
            {icon_upload}
            <span>Carregue a planilha Excel (.xlsx) no painel acima para iniciar</span>
        </div>
    </div>
    """)
    st.html(html)
