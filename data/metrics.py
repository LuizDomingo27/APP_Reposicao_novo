# ═══════════════════════════════════════════════════════════════════════════════
# METRICS & AGGREGATIONS — Business logic with guaranteed fallback contracts
# ═══════════════════════════════════════════════════════════════════════════════

from typing import Dict, List, Tuple, Any
import pandas as pd
from config.tokens import MESES_PT, STATUS_COLORS

STATUS_FINALIZADO = "Finalizado"
STATUS_EM_ANDAMENTO = "Em Andamento"


def get_chamados_kpis(df_filtered: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes the headline "Chamados" KPIs safely:
      • total_chamados      — number of reposição requests in the period
      • finalizados         — chamados answered: COMPLETA or INCOMPLETA (STATUS_CHAMADO == Finalizado)
      • em_andamento        — chamados not yet finalised
      • taxa_finalizacao    — % of chamados finalised
      • total_pecas         — sum of requested pieces (outliers already stripped in loader)
      • media_pecas         — average pieces per chamado with a valid quantity
    """
    default = {
        "total_chamados": 0,
        "finalizados": 0,
        "em_andamento": 0,
        "taxa_finalizacao": 0.0,
        "total_pecas": 0,
        "media_pecas": 0.0,
    }
    if df_filtered is None or df_filtered.empty:
        return default

    try:
        total_chamados = len(df_filtered)
        if total_chamados == 0:
            return default

        if "STATUS_CHAMADO" in df_filtered.columns:
            finalizados = int((df_filtered["STATUS_CHAMADO"] == STATUS_FINALIZADO).sum())
        else:
            finalizados = 0
        em_andamento = total_chamados - finalizados
        taxa_finalizacao = (finalizados / total_chamados) * 100 if total_chamados else 0.0

        total_pecas = 0
        media_pecas = 0.0
        if "QUANTIDADE" in df_filtered.columns:
            qty = pd.to_numeric(df_filtered["QUANTIDADE"], errors="coerce").dropna()
            if not qty.empty:
                total_pecas = int(qty.sum())
                media_pecas = float(qty.mean())

        return {
            "total_chamados": total_chamados,
            "finalizados": finalizados,
            "em_andamento": em_andamento,
            "taxa_finalizacao": float(taxa_finalizacao),
            "total_pecas": total_pecas,
            "media_pecas": media_pecas,
        }
    except Exception:
        return default


def _top_value(series: pd.Series, ignore=("", "NÃO INFORMADA", "NÃO INFORMADO")) -> Tuple[str, int]:
    """Returns (value, count) for the most frequent non-empty entry of a series."""
    if series is None or series.empty:
        return ("N/A", 0)
    counts = series.dropna().astype(str).str.strip()
    counts = counts[~counts.str.upper().isin([v.upper() for v in ignore])].value_counts()
    if counts.empty:
        return ("N/A", 0)
    return (str(counts.index[0]), int(counts.iloc[0]))


def get_highlights(df_filtered: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes the highlight cards safely:
      • top_oficina  — workshop that requested the most reposições (+ its count)
      • top_motivo   — most frequent reposição motive (+ its count)
    """
    default = {
        "top_oficina": "N/A", "top_oficina_count": 0,
        "top_motivo": "N/A", "top_motivo_count": 0,
    }
    if df_filtered is None or df_filtered.empty:
        return default

    try:
        result = dict(default)
        if "OFICINA" in df_filtered.columns:
            name, count = _top_value(df_filtered["OFICINA"])
            result["top_oficina"] = name.title() if name != "N/A" else "N/A"
            result["top_oficina_count"] = count
        if "MOTIVO" in df_filtered.columns:
            name, count = _top_value(df_filtered["MOTIVO"])
            result["top_motivo"] = name.title() if name != "N/A" else "N/A"
            result["top_motivo_count"] = count
        return result
    except Exception:
        return default


def get_status_distribution(df_filtered: pd.DataFrame) -> Dict[str, Any]:
    """Returns labels/values/colors for the Status dos Chamados donut."""
    default: Dict[str, Any] = {"labels": [], "values": [], "colors": []}
    if df_filtered is None or df_filtered.empty or "STATUS_CHAMADO" not in df_filtered.columns:
        return default

    try:
        finalizados = int((df_filtered["STATUS_CHAMADO"] == STATUS_FINALIZADO).sum())
        em_andamento = int((df_filtered["STATUS_CHAMADO"] == STATUS_EM_ANDAMENTO).sum())

        labels, values, colors = [], [], []
        for label, value in ((STATUS_FINALIZADO, finalizados), (STATUS_EM_ANDAMENTO, em_andamento)):
            if value > 0:
                labels.append(label)
                values.append(value)
                colors.append(STATUS_COLORS.get(label, "#999999"))

        return {"labels": labels, "values": values, "colors": colors}
    except Exception:
        return default


def get_rankings(df_filtered: pd.DataFrame, top_n: int = 3) -> Dict[str, List[Tuple[str, int, float]]]:
    """Calculates Top N Raw Material lines and Top N Requested Garment Parts safely."""
    default: Dict[str, List[Tuple[str, int, float]]] = {"mp_data": [], "parte_data": []}
    if df_filtered is None or df_filtered.empty:
        return default

    try:
        # Top MP
        mp_data = []
        if "MP" in df_filtered.columns:
            mp_counts = df_filtered["MP"].dropna().value_counts()
            mp_total = mp_counts.sum()
            if mp_total > 0:
                mp_data = [
                    (str(name), int(count), float((count / mp_total) * 100))
                    for name, count in mp_counts.head(top_n).items()
                ]

        # Top Partes da Peça
        parte_data = []
        if "PARTE_PECA" in df_filtered.columns:
            parte_counts = df_filtered["PARTE_PECA"].dropna().value_counts()
            parte_total = parte_counts.sum()
            if parte_total > 0:
                parte_data = [
                    (str(name), int(count), float((count / parte_total) * 100))
                    for name, count in parte_counts.head(top_n).items()
                ]

        return {
            "mp_data": mp_data,
            "parte_data": parte_data
        }
    except Exception:
        return default


def get_monthly_history(df_repo: pd.DataFrame, n_months: int = 3) -> Dict[str, Any]:
    """Calculates historical monthly totals for the last N months safely."""
    default = {"labels": [], "values": [], "table_data": []}
    if df_repo is None or df_repo.empty or "DATA" not in df_repo.columns:
        return default

    try:
        df_temp = df_repo.dropna(subset=["DATA"]).copy()
        if not pd.api.types.is_datetime64_any_dtype(df_temp["DATA"]):
            df_temp["DATA"] = pd.to_datetime(df_temp["DATA"], errors="coerce")
            df_temp = df_temp.dropna(subset=["DATA"])

        if df_temp.empty:
            return default

        df_temp["MES_ANO"] = df_temp["DATA"].dt.to_period("M")
        all_months = df_temp["MES_ANO"].value_counts().sort_index()
        last_months = all_months.tail(n_months)

        labels = []
        values = []
        table_data = []

        for period_key, count in last_months.items():
            month_num = period_key.month
            month_name = MESES_PT.get(month_num, str(month_num))[:3]
            labels.append(f"{month_name}/{period_key.year}")
            values.append(int(count))
            table_data.append((f"{str(month_num).zfill(2)}/{period_key.year}", int(count)))

        return {
            "labels": labels,
            "values": values,
            "table_data": table_data
        }
    except Exception:
        return default


def get_weekly_distribution(df_filtered: pd.DataFrame, max_weeks: int = 12) -> Dict[str, List]:
    """Aggregates requests by ISO week within the filtered dataset safely."""
    default: Dict[str, List] = {"labels": [], "values": []}
    if df_filtered is None or df_filtered.empty or "DATA" not in df_filtered.columns:
        return default

    try:
        df_temp = df_filtered.dropna(subset=["DATA"]).copy()
        if not pd.api.types.is_datetime64_any_dtype(df_temp["DATA"]):
            df_temp["DATA"] = pd.to_datetime(df_temp["DATA"], errors="coerce")
            df_temp = df_temp.dropna(subset=["DATA"])

        if df_temp.empty:
            return default

        df_temp["SEMANA"] = df_temp["DATA"].dt.isocalendar().week.astype(int)
        df_temp["ANO"] = df_temp["DATA"].dt.year

        weekly = df_temp.groupby(["ANO", "SEMANA"]).size().reset_index(name="TOTAL")
        weekly = weekly.sort_values(["ANO", "SEMANA"]).tail(max_weeks)

        labels = [f"S{int(row['SEMANA'])}" for _, row in weekly.iterrows()]
        values = [int(row["TOTAL"]) for _, row in weekly.iterrows()]

        return {
            "labels": labels,
            "values": values
        }
    except Exception:
        return default
