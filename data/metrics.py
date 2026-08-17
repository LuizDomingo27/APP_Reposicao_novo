# ═══════════════════════════════════════════════════════════════════════════════
# METRICS & AGGREGATIONS — Business logic with guaranteed fallback contracts
# ═══════════════════════════════════════════════════════════════════════════════

from typing import Dict, List, Tuple, Any
import pandas as pd
from config.tokens import MESES_PT


def get_kpis(df_filtered: pd.DataFrame) -> Dict[str, Any]:
    """Calculates total requests and the top requesting workshop safely."""
    default = {
        "total_repo": 0,
        "top_oficina": "N/A",
        "top_oficina_count": 0
    }
    if df_filtered is None or df_filtered.empty or "OFICINA" not in df_filtered.columns:
        return default

    try:
        total_repo = len(df_filtered)
        if total_repo == 0:
            return default

        oficina_counts = df_filtered["OFICINA"].dropna().value_counts()
        if oficina_counts.empty:
            return default

        top_oficina_raw = str(oficina_counts.index[0])
        top_oficina_count = int(oficina_counts.iloc[0])

        top_oficina_display = top_oficina_raw.title()
        if len(top_oficina_display) > 50:
            top_oficina_display = top_oficina_display[:47] + "..."

        return {
            "total_repo": total_repo,
            "top_oficina": top_oficina_display,
            "top_oficina_count": top_oficina_count
        }
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


def get_negadas_metrics(df_neg_filtered: pd.DataFrame) -> Dict[str, Any]:
    """Calculates total rejections, total pieces denied, and average pieces per rejection safely."""
    default = {"total_negadas": 0, "total_pecas": 0, "media_pecas": 0.0}
    if df_neg_filtered is None or df_neg_filtered.empty:
        return default

    try:
        total_negadas = len(df_neg_filtered)
        total_pecas = 0
        media_pecas = 0.0
        if "QTD_EXTRAIDA" in df_neg_filtered.columns:
            valid_series = pd.to_numeric(df_neg_filtered["QTD_EXTRAIDA"], errors="coerce").dropna()
            if not valid_series.empty:
                total_pecas = int(valid_series.sum())
                media_pecas = float(valid_series.mean())

        return {
            "total_negadas": total_negadas,
            "total_pecas": total_pecas,
            "media_pecas": media_pecas
        }
    except Exception:
        return default


def get_negadas_distribution(df_neg_filtered: pd.DataFrame, max_weeks: int = 12) -> Dict[str, Any]:
    """
    Aggregates denied requests and total pieces by week and month safely.
    Returns labels and values for both counts and pieces.
    """
    default = {
        "weekly_negadas_labels": [],
        "weekly_negadas_values": [],
        "weekly_pecas_labels": [],
        "weekly_pecas_values": [],
        "monthly_negadas_labels": [],
        "monthly_negadas_values": [],
        "monthly_pecas_labels": [],
        "monthly_pecas_values": [],
    }
    if df_neg_filtered is None or df_neg_filtered.empty or "DATA" not in df_neg_filtered.columns:
        return default

    try:
        df_temp = df_neg_filtered.dropna(subset=["DATA"]).copy()
        if not pd.api.types.is_datetime64_any_dtype(df_temp["DATA"]):
            df_temp["DATA"] = pd.to_datetime(df_temp["DATA"], errors="coerce")
            df_temp = df_temp.dropna(subset=["DATA"])

        if df_temp.empty:
            return default

        # Numeric pieces column
        if "QTD_EXTRAIDA" in df_temp.columns:
            df_temp["QTD_NUM"] = pd.to_numeric(df_temp["QTD_EXTRAIDA"], errors="coerce").fillna(1).astype(int)
        else:
            df_temp["QTD_NUM"] = 1

        # Weekly aggregation
        df_temp["SEMANA"] = df_temp["DATA"].dt.isocalendar().week.astype(int)
        df_temp["ANO"] = df_temp["DATA"].dt.year

        weekly = df_temp.groupby(["ANO", "SEMANA"]).agg(
            TOTAL_NEGADAS=("DATA", "count"),
            TOTAL_PECAS=("QTD_NUM", "sum")
        ).reset_index()
        weekly = weekly.sort_values(["ANO", "SEMANA"]).tail(max_weeks)

        weekly_labels = [f"S{int(row['SEMANA'])}" for _, row in weekly.iterrows()]
        weekly_negadas_vals = [int(row["TOTAL_NEGADAS"]) for _, row in weekly.iterrows()]
        weekly_pecas_vals = [int(row["TOTAL_PECAS"]) for _, row in weekly.iterrows()]

        # Monthly aggregation
        df_temp["MES_ANO"] = df_temp["DATA"].dt.to_period("M")
        monthly = df_temp.groupby("MES_ANO").agg(
            TOTAL_NEGADAS=("DATA", "count"),
            TOTAL_PECAS=("QTD_NUM", "sum")
        ).reset_index()
        monthly = monthly.sort_values("MES_ANO").tail(6)

        monthly_labels = []
        for _, row in monthly.iterrows():
            p = row["MES_ANO"]
            m_name = MESES_PT.get(p.month, str(p.month))[:3]
            monthly_labels.append(f"{m_name}/{p.year}")

        monthly_negadas_vals = [int(row["TOTAL_NEGADAS"]) for _, row in monthly.iterrows()]
        monthly_pecas_vals = [int(row["TOTAL_PECAS"]) for _, row in monthly.iterrows()]

        return {
            "weekly_negadas_labels": weekly_labels,
            "weekly_negadas_values": weekly_negadas_vals,
            "weekly_pecas_labels": weekly_labels,
            "weekly_pecas_values": weekly_pecas_vals,
            "monthly_negadas_labels": monthly_labels,
            "monthly_negadas_values": monthly_negadas_vals,
            "monthly_pecas_labels": monthly_labels,
            "monthly_pecas_values": monthly_pecas_vals,
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
