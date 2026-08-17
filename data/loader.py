# ═══════════════════════════════════════════════════════════════════════════════
# DATA LOADER — Reads, validates, and normalises the Excel workbook
# ═══════════════════════════════════════════════════════════════════════════════

import logging
import pandas as pd
import streamlit as st

from config.tokens import QUANTIDADE_OUTLIER_CAP

logger = logging.getLogger(__name__)

# Standard expected schema for the primary "Chamados" (reposições) sheet.
# SITUACAO       — raw completion status from the "REPOSIÇÃO" column (COMPLETA / INCOMPLETA / ...)
# STATUS_CHAMADO — derived operational status used across the dashboard (Finalizado / Em Andamento)
REPOSICOES_COLUMNS = [
    "OFICINA", "MP", "PARTE_PECA", "MOTIVO", "QUANTIDADE", "DATA", "SITUACAO", "STATUS_CHAMADO"
]

# Operational status labels (single source of truth)
STATUS_FINALIZADO = "Finalizado"
STATUS_EM_ANDAMENTO = "Em Andamento"


class DataLoadError(Exception):
    """Base exception for data loading errors."""
    pass


class InvalidFileError(DataLoadError):
    """Raised when the uploaded file is not a readable Excel file."""
    pass


class MissingSheetError(DataLoadError):
    """Raised when a required worksheet is missing."""
    pass


@st.cache_data(show_spinner="Processando planilha...")
def load_data(file) -> pd.DataFrame:
    """
    Parse the uploaded Excel file and return a single clean, validated DataFrame
    of "chamados" (reposições) from the primary REPOSIÇÕES sheet.
    """
    if file is None:
        return _empty_repo_df()

    try:
        excel_file = pd.ExcelFile(file, engine="openpyxl")
    except Exception as e:
        logger.error(f"Erro ao abrir arquivo Excel: {e}")
        raise InvalidFileError(f"O arquivo fornecido não é uma planilha Excel válida: {e}")

    return _load_reposicoes(excel_file)


# ── Private Loaders & Normalisers ───────────────────────────────────────────────

def _load_reposicoes(excel_file: pd.ExcelFile) -> pd.DataFrame:
    """Load and normalise the primary REPOSIÇÕES sheet into the Chamados schema."""
    try:
        # Prefer sheet named 'REPOSIÇÕES' or 'REPOSICOES', fallback to sheet 0
        sheet_name = 0
        for s in excel_file.sheet_names:
            if "REPOSI" in s.strip().upper():
                sheet_name = s
                break

        df = pd.read_excel(excel_file, sheet_name=sheet_name, engine="openpyxl")
    except Exception as e:
        logger.error(f"Falha ao ler aba principal de reposições: {e}")
        raise MissingSheetError(f"Não foi possível ler a aba de reposições: {e}")

    if df.empty:
        return _empty_repo_df()

    # Normalize column names. The real workbook exposes the completion status in
    # the "REPOSIÇÃO" column (COMPLETA / INCOMPLETA / vazio) — NOT the "STATUS"
    # column, which is a mostly-empty material-code field and is discarded here.
    col_map = {}
    for c in df.columns:
        cu = str(c).strip().upper()
        if cu == "OFICINA":
            col_map[c] = "OFICINA"
        elif cu == "MP":
            col_map[c] = "MP"
        elif "PARTE" in cu and "PE" in cu:
            col_map[c] = "PARTE_PECA"
        elif "MOTIVO" in cu:
            col_map[c] = "MOTIVO"
        elif cu == "QUANTIDADE" or cu == "QTD":
            col_map[c] = "QUANTIDADE"
        elif cu == "DATA":
            col_map[c] = "DATA"
        elif cu == "REPOSIÇÃO" or cu == "REPOSICAO":
            col_map[c] = "SITUACAO"
    df = df.rename(columns=col_map)

    # Ensure required source columns exist
    for col in ["OFICINA", "MP", "PARTE_PECA", "MOTIVO", "QUANTIDADE", "DATA", "SITUACAO"]:
        if col not in df.columns:
            df[col] = pd.NA

    # Parse and sanitize Date column (guarantee timezone-naive datetime64)
    df["DATA"] = pd.to_datetime(df["DATA"], dayfirst=True, errors="coerce")
    if hasattr(df["DATA"].dt, "tz") and df["DATA"].dt.tz is not None:
        df["DATA"] = df["DATA"].dt.tz_localize(None)
    df = df.dropna(subset=["DATA"])

    # Sanitize and cast text columns
    df["OFICINA"] = df["OFICINA"].fillna("NÃO INFORMADA").astype(str).str.strip().str.upper()
    df["MP"] = df["MP"].fillna("NÃO INFORMADA").astype(str).str.strip().str.upper()
    df["PARTE_PECA"] = df["PARTE_PECA"].fillna("NÃO INFORMADA").astype(str).str.strip().str.title()
    # Normalise motive to upper-case so case-only variants collapse together
    # (e.g. "Material não enviado..." and "MATERIAL NÃO ENVIADO..." count as one).
    df["MOTIVO"] = df["MOTIVO"].fillna("").astype(str).str.strip().str.upper()
    df["SITUACAO"] = df["SITUACAO"].fillna("").astype(str).str.strip().str.upper()

    # Derive the operational status: a chamado is "Finalizado" when the workshop
    # answered it — either COMPLETA or INCOMPLETA (both are attended outcomes,
    # matching how the RESUMO tab sums Completas + Incompletas). Everything else
    # (blank / not-yet-answered records) counts as still open.
    _finalizado = {"COMPLETA", "INCOMPLETA"}
    df["STATUS_CHAMADO"] = df["SITUACAO"].apply(
        lambda s: STATUS_FINALIZADO if s in _finalizado else STATUS_EM_ANDAMENTO
    )

    # Sanitize Quantity — the source sheet contains data-entry errors (values up
    # to 10.000.000). Coerce, drop negatives and implausible outliers to NaN so
    # piece totals stay meaningful. NaN is preserved (not filled) so it is simply
    # excluded from sums/means downstream.
    q = pd.to_numeric(df["QUANTIDADE"], errors="coerce")
    df["QUANTIDADE"] = q.where((q >= 0) & (q < QUANTIDADE_OUTLIER_CAP))

    return df[REPOSICOES_COLUMNS].reset_index(drop=True)


def _empty_repo_df() -> pd.DataFrame:
    """Returns an empty DataFrame matching the Chamados schema."""
    return pd.DataFrame(columns=REPOSICOES_COLUMNS)
