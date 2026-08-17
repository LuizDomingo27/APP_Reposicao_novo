# ═══════════════════════════════════════════════════════════════════════════════
# DATA FILTERS — Logic for robust date and period based data slicing
# ═══════════════════════════════════════════════════════════════════════════════

import calendar
from datetime import datetime, date, timedelta
from typing import Optional, Union
import pandas as pd


def filter_by_date_range(
    df: pd.DataFrame,
    col: str = "DATA",
    start_date: Optional[Union[datetime, date, pd.Timestamp, str]] = None,
    end_date: Optional[Union[datetime, date, pd.Timestamp, str]] = None,
) -> pd.DataFrame:
    """
    Safely filters a DataFrame by date range [start_date, end_date].
    Inclusive of full start day (00:00:00) and full end day (23:59:59.999999).
    """
    if df is None or df.empty or col not in df.columns:
        return pd.DataFrame() if df is None else df.copy()

    df_clean = df.copy()
    if not pd.api.types.is_datetime64_any_dtype(df_clean[col]):
        df_clean[col] = pd.to_datetime(df_clean[col], errors="coerce")

    if hasattr(df_clean[col].dt, "tz") and df_clean[col].dt.tz is not None:
        df_clean[col] = df_clean[col].dt.tz_localize(None)

    resolved_start = _resolve_ref_date(start_date) if start_date is not None else None
    resolved_end = _resolve_ref_date(end_date) if end_date is not None else None

    if resolved_start is None and resolved_end is None:
        return df_clean

    mask = pd.Series(True, index=df_clean.index)

    if resolved_start is not None:
        start_ts = pd.Timestamp(resolved_start.replace(hour=0, minute=0, second=0, microsecond=0))
        mask &= (df_clean[col] >= start_ts)

    if resolved_end is not None:
        end_ts = pd.Timestamp(resolved_end.replace(hour=23, minute=59, second=59, microsecond=999999))
        mask &= (df_clean[col] <= end_ts)

    return df_clean[mask].reset_index(drop=True)


def filter_by_period(
    df: pd.DataFrame,
    col: str = "DATA",
    period: str = "Mês",
    ref_date: Optional[Union[datetime, date, pd.Timestamp, str]] = None,
    start_date: Optional[Union[datetime, date, pd.Timestamp, str]] = None,
    end_date: Optional[Union[datetime, date, pd.Timestamp, str]] = None,
) -> pd.DataFrame:
    """
    Safely filters a DataFrame by selected period ('Dia', 'Semana', 'Mês', 'Intervalo', 'Tudo')
    or explicit date range [start_date, end_date]. Handles timezone, missing data, and type edge cases.
    """
    if period in ["Intervalo", "Personalizado", "Customizado"] or (start_date is not None or end_date is not None):
        return filter_by_date_range(df, col=col, start_date=start_date, end_date=end_date)

    if period in ["Tudo", "Todos", "Todo o Período"]:
        return filter_by_date_range(df, col=col, start_date=None, end_date=None)

    resolved_ref = _resolve_ref_date(ref_date, df[col] if df is not None and col in df.columns else None)
    if resolved_ref is None:
        return df_clean if 'df_clean' in locals() else (df.copy() if df is not None else pd.DataFrame())

    try:
        if period == "Dia":
            s_date = resolved_ref.date()
            e_date = resolved_ref.date()
        elif period == "Semana":
            s_date = (resolved_ref - timedelta(days=resolved_ref.weekday())).date()
            e_date = s_date + timedelta(days=6)
        elif period == "Mês":
            s_date = resolved_ref.replace(day=1).date()
            last_day = calendar.monthrange(resolved_ref.year, resolved_ref.month)[1]
            e_date = resolved_ref.replace(day=last_day).date()
        else:
            return df.copy() if df is not None else pd.DataFrame()
    except Exception:
        return df.copy() if df is not None else pd.DataFrame()

    return filter_by_date_range(df, col=col, start_date=s_date, end_date=e_date)


def get_date_range_label(
    start_date: Optional[Union[datetime, date, pd.Timestamp, str]] = None,
    end_date: Optional[Union[datetime, date, pd.Timestamp, str]] = None,
) -> str:
    """Generates a human-readable string label for a date range interval (De X até Y)."""
    s_dt = _resolve_ref_date(start_date) if start_date is not None else None
    e_dt = _resolve_ref_date(end_date) if end_date is not None else None

    if s_dt and e_dt:
        if s_dt.date() == e_dt.date():
            return s_dt.strftime("%d/%m/%Y")
        return f"{s_dt.strftime('%d/%m/%Y')} à {e_dt.strftime('%d/%m/%Y')}"
    elif s_dt:
        return f"A partir de {s_dt.strftime('%d/%m/%Y')}"
    elif e_dt:
        return f"Até {e_dt.strftime('%d/%m/%Y')}"
    else:
        return "Todo o Período"


def get_period_label(
    period: str = "Intervalo",
    ref_date: Optional[Union[datetime, date, pd.Timestamp, str]] = None,
    start_date: Optional[Union[datetime, date, pd.Timestamp, str]] = None,
    end_date: Optional[Union[datetime, date, pd.Timestamp, str]] = None,
) -> str:
    """Generates a human-readable string label for the current filter window."""
    if start_date is not None or end_date is not None or period in ["Intervalo", "Personalizado"]:
        return get_date_range_label(start_date, end_date)

    if period in ["Tudo", "Todos", "Todo o Período"]:
        return "Todo o Período"

    resolved_ref = _resolve_ref_date(ref_date)
    if resolved_ref is None:
        resolved_ref = datetime.today()

    try:
        if period == "Dia":
            return resolved_ref.strftime("%d/%m/%Y")
        elif period == "Semana":
            start = resolved_ref - timedelta(days=resolved_ref.weekday())
            end = start + timedelta(days=6)
            return f"{start.strftime('%d/%m')} à {end.strftime('%d/%m/%Y')}"
        elif period == "Mês":
            last_day = calendar.monthrange(resolved_ref.year, resolved_ref.month)[1]
            return f"01 à {last_day:02d}/{resolved_ref.strftime('%m/%Y')}"
    except Exception:
        return ""
    return ""


def _resolve_ref_date(
    ref_date: Optional[Union[datetime, date, pd.Timestamp, str]],
    fallback_series: Optional[pd.Series] = None
) -> Optional[datetime]:
    """Helper to convert any date representation to a timezone-naive datetime."""
    if ref_date is None:
        if fallback_series is not None and not fallback_series.dropna().empty:
            max_val = fallback_series.max()
            if isinstance(max_val, pd.Timestamp):
                return max_val.to_pydatetime().replace(tzinfo=None)
        return datetime.today()

    if isinstance(ref_date, pd.Timestamp):
        dt = ref_date.to_pydatetime()
    elif isinstance(ref_date, datetime):
        dt = ref_date
    elif isinstance(ref_date, date):
        dt = datetime.combine(ref_date, datetime.min.time())
    elif isinstance(ref_date, str):
        parsed = pd.to_datetime(ref_date, errors="coerce")
        if pd.isna(parsed):
            return datetime.today()
        dt = parsed.to_pydatetime()
    else:
        return datetime.today()

    # Ensure timezone-naive
    if hasattr(dt, "tzinfo") and dt.tzinfo is not None:
        dt = dt.replace(tzinfo=None)

    return dt

