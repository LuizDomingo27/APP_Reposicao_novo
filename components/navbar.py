# ═══════════════════════════════════════════════════════════════════════════════
# COMPONENT: NAVBAR — Modern top navigation bar (Header, Upload, and Date Filters)
# Replaces legacy sidebar with a sleek, unified top control panel
# ═══════════════════════════════════════════════════════════════════════════════

import textwrap
import calendar
from datetime import datetime, date, timedelta
from typing import Tuple, Any, Optional
import streamlit as st
from config.tokens import COLORS, FONT_FAMILY, FONT_CDN
from config.icons import get_svg_icon


def render_navbar() -> Tuple[Any, Optional[date], Optional[date], str]:
    """
    Renders the unified top navigation bar with branding, dataset uploader,
    and dynamic period/date range controls without sidebar.
    """
    icon_logo = get_svg_icon("logo", size=26, color=COLORS["orange"])
    icon_upload = get_svg_icon("upload", size=16, color=COLORS["orange"])
    icon_filter = get_svg_icon("filter", size=16, color=COLORS["green_accent"])

    navbar_html = textwrap.dedent(f"""
    <link href="{FONT_CDN}" rel="stylesheet">
    <div style="
        font-family: {FONT_FAMILY};
        background: linear-gradient(135deg, {COLORS['green_dark']} 0%, {COLORS['green_mid']} 100%);
        border-radius: 16px;
        padding: 16px 24px;
        color: white;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 20px rgba(27, 58, 45, 0.14);
        margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    ">
        <div style="display: flex; align-items: center; gap: 14px;">
            <div style="
                width: 44px;
                height: 44px;
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
            ">
                {icon_logo}
            </div>
            <div>
                <div style="
                    font-size: 1.15rem;
                    font-weight: 800;
                    color: #FFFFFF;
                    letter-spacing: -0.01em;
                    line-height: 1.1;
                ">
                    GESTÃO DE OFICINAS
                </div>
                <div style="
                    font-size: 0.76rem;
                    color: rgba(255, 255, 255, 0.6);
                    font-weight: 400;
                    letter-spacing: 0.04em;
                    text-transform: uppercase;
                ">
                    Painel Corporativo de Reposições
                </div>
            </div>
        </div>
        <div style="
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.75rem;
            color: rgba(255, 255, 255, 0.7);
            background: rgba(0, 0, 0, 0.15);
            padding: 6px 14px;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.08);
        ">
            <span>Controle e Auditoria Operacional</span>
        </div>
    </div>
    """)
    st.html(navbar_html)

    # Controls Container (Upload + Dynamic Filters)
    with st.container():
        ctrl_col1, ctrl_col2, ctrl_col3, ctrl_col4 = st.columns([1.4, 1.0, 0.8, 0.8], gap="medium")

        with ctrl_col1:
            uploaded_file = st.file_uploader(
                "Carregar Planilha (.xlsx)",
                type=["xlsx"],
                help="Selecione o arquivo Excel de reposições diárias",
                label_visibility="visible"
            )

        with ctrl_col2:
            period_type = st.selectbox(
                "Filtro de Período",
                options=["Todo o Período", "Intervalo (De / Até)", "Mês Atual", "Semana Atual", "Dia Específico"],
                index=0,
                help="Escolha o modo de filtragem temporal"
            )

        start_date: Optional[date] = None
        end_date: Optional[date] = None
        today = datetime.today().date()

        if period_type == "Intervalo (De / Até)":
            with ctrl_col3:
                start_date = st.date_input(
                    "Data Inicial",
                    value=date(today.year, today.month, 1),
                    help="Início do intervalo de análise",
                    format="DD/MM/YYYY"
                )
            with ctrl_col4:
                end_date = st.date_input(
                    "Data Final",
                    value=today,
                    help="Fim do intervalo de análise",
                    format="DD/MM/YYYY"
                )
        elif period_type == "Mês Atual":
            with ctrl_col3:
                ref_date = st.date_input(
                    "Data de Referência",
                    value=today,
                    help="Selecione um dia do mês desejado",
                    format="DD/MM/YYYY"
                )
            start_date = date(ref_date.year, ref_date.month, 1)
            last_day = calendar.monthrange(ref_date.year, ref_date.month)[1]
            end_date = date(ref_date.year, ref_date.month, last_day)
            with ctrl_col4:
                st.markdown(
                    f"<div style='padding-top: 28px; font-size: 0.8rem; font-weight: 600; color: {COLORS['text_secondary']};'>"
                    f"Mês Completo</div>",
                    unsafe_allow_html=True
                )
        elif period_type == "Semana Atual":
            with ctrl_col3:
                ref_date = st.date_input(
                    "Data de Referência",
                    value=today,
                    help="Selecione um dia da semana desejada",
                    format="DD/MM/YYYY"
                )
            start_date = ref_date - timedelta(days=ref_date.weekday())
            end_date = start_date + timedelta(days=6)
            with ctrl_col4:
                st.markdown(
                    f"<div style='padding-top: 28px; font-size: 0.8rem; font-weight: 600; color: {COLORS['text_secondary']};'>"
                    f"Semana Completa</div>",
                    unsafe_allow_html=True
                )
        elif period_type == "Dia Específico":
            with ctrl_col3:
                ref_date = st.date_input(
                    "Data do Dia",
                    value=today,
                    help="Selecione o dia exato de análise",
                    format="DD/MM/YYYY"
                )
            start_date = ref_date
            end_date = ref_date
            with ctrl_col4:
                st.markdown(
                    f"<div style='padding-top: 28px; font-size: 0.8rem; font-weight: 600; color: {COLORS['text_secondary']};'>"
                    f"Dia Único</div>",
                    unsafe_allow_html=True
                )
        elif period_type == "Todo o Período":
            start_date = None
            end_date = None
            with ctrl_col3:
                st.markdown(
                    f"<div style='padding-top: 28px; font-size: 0.8rem; font-weight: 600; color: {COLORS['text_secondary']};'>"
                    f"Sem filtro inicial</div>",
                    unsafe_allow_html=True
                )
            with ctrl_col4:
                st.markdown(
                    f"<div style='padding-top: 28px; font-size: 0.8rem; font-weight: 600; color: {COLORS['text_secondary']};'>"
                    f"Sem filtro final</div>",
                    unsafe_allow_html=True
                )

    st.markdown("<div style='height: 8px'></div>", unsafe_allow_html=True)
    return uploaded_file, start_date, end_date, period_type
