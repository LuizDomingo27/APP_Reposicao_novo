# ═══════════════════════════════════════════════════════════════════════════════
# COMPONENT: SIDEBAR — User control panel (file upload, period and date selectors)
# ═══════════════════════════════════════════════════════════════════════════════

import textwrap
import calendar
from datetime import datetime, date, timedelta
from typing import Tuple, Any, Optional
import streamlit as st
from config.tokens import COLORS
from config.icons import get_svg_icon


def render_sidebar() -> Tuple[Any, Optional[date], Optional[date], str]:
    """Renders the sidebar navigation with modern styling and dynamic date range selector."""
    icon_logo = get_svg_icon("logo", size=24, color=COLORS["orange"])

    with st.sidebar:
        header_html = textwrap.dedent(f"""
        <div style="
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 4px 20px 4px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 20px;
        ">
            <div style="
                width: 40px;
                height: 40px;
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
            ">
                {icon_logo}
            </div>
            <div>
                <div style="
                    font-size: 0.95rem;
                    font-weight: 700;
                    color: #FFFFFF;
                    letter-spacing: 0.04em;
                    text-transform: uppercase;
                ">Reposições</div>
                <div style="
                    font-size: 0.72rem;
                    color: rgba(255, 255, 255, 0.5);
                    font-weight: 400;
                ">Gestão de Oficinas</div>
            </div>
        </div>
        """)
        st.html(header_html)

        uploaded_file = st.file_uploader(
            "Planilha de Dados (.xlsx)",
            type=["xlsx"],
            help="Carregue o arquivo de reposições diárias"
        )

        st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)

        period_type = st.selectbox(
            "Filtro de Período",
            options=["Intervalo (De / Até)", "Mês Atual", "Semana Atual", "Dia Específico", "Todo o Período"],
            index=0,
            help="Escolha o modo de filtragem temporal dos relatórios"
        )

        st.markdown("<div style='height: 8px'></div>", unsafe_allow_html=True)

        start_date: Optional[date] = None
        end_date: Optional[date] = None
        today = datetime.today().date()

        if period_type == "Intervalo (De / Até)":
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input(
                    "Data Inicial",
                    value=date(today.year, today.month, 1),
                    help="Início do intervalo de análise",
                    format="DD/MM/YYYY"
                )
            with col2:
                end_date = st.date_input(
                    "Data Final",
                    value=today,
                    help="Fim do intervalo de análise",
                    format="DD/MM/YYYY"
                )
        elif period_type == "Mês Atual":
            ref_date = st.date_input(
                "Data de Referência",
                value=today,
                help="Selecione um dia do mês desejado",
                format="DD/MM/YYYY"
            )
            start_date = date(ref_date.year, ref_date.month, 1)
            last_day = calendar.monthrange(ref_date.year, ref_date.month)[1]
            end_date = date(ref_date.year, ref_date.month, last_day)
        elif period_type == "Semana Atual":
            ref_date = st.date_input(
                "Data de Referência",
                value=today,
                help="Selecione um dia da semana desejada",
                format="DD/MM/YYYY"
            )
            start_date = ref_date - timedelta(days=ref_date.weekday())
            end_date = start_date + timedelta(days=6)
        elif period_type == "Dia Específico":
            ref_date = st.date_input(
                "Data do Dia",
                value=today,
                help="Selecione o dia exato de análise",
                format="DD/MM/YYYY"
            )
            start_date = ref_date
            end_date = ref_date
        elif period_type == "Todo o Período":
            start_date = None
            end_date = None

        footer_html = textwrap.dedent("""
        <div style="
            margin-top: 36px;
            padding: 14px;
            background: rgba(0, 0, 0, 0.15);
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.06);
            font-size: 0.72rem;
            color: rgba(255, 255, 255, 0.45);
            line-height: 1.4;
        ">
            Painel corporativo para monitoramento e auditoria de reposição de peças de corte e costura.
        </div>
        """)
        st.html(footer_html)

    return uploaded_file, start_date, end_date, period_type

