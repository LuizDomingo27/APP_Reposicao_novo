# ═══════════════════════════════════════════════════════════════════════════════
# DATA LOADER — Reads, validates, and normalises the Excel workbook
# ═══════════════════════════════════════════════════════════════════════════════

import re
import logging
from typing import Tuple, Optional
import pandas as pd
import streamlit as st

logger = logging.getLogger(__name__)

# Standard expected schemas
REPOSICOES_COLUMNS = ["OFICINA", "MP", "PARTE_PECA", "QUANTIDADE", "DATA", "STATUS"]
NEGADAS_COLUMNS = ["TAREFA", "DATA_CRIACAO", "DESCRICAO", "DATA", "QTD_EXTRAIDA", "PARTE_PECA"]


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
def load_data(file) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Parse the uploaded Excel file and return two clean, validated DataFrames:
      • df_repo  — from the primary REPOSIÇÕES sheet
      • df_neg   — from the NEGADAS sheet (or empty DataFrame if missing)
    """
    if file is None:
        return _empty_repo_df(), _empty_neg_df()

    try:
        excel_file = pd.ExcelFile(file, engine="openpyxl")
    except Exception as e:
        logger.error(f"Erro ao abrir arquivo Excel: {e}")
        raise InvalidFileError(f"O arquivo fornecido não é uma planilha Excel válida: {e}")

    df_repo = _load_reposicoes(excel_file)
    df_neg = _load_negadas(excel_file)

    return df_repo, df_neg


# ── Private Loaders & Normalisers ───────────────────────────────────────────────

def _load_reposicoes(excel_file: pd.ExcelFile) -> pd.DataFrame:
    """Load and normalise the primary REPOSIÇÕES sheet."""
    try:
        # Prefer sheet named 'REPOSIÇÕES' or 'REPOSICOES', fallback to sheet 0
        sheet_name = 0
        for s in excel_file.sheet_names:
            s_clean = s.strip().upper()
            if "REPOSI" in s_clean:
                sheet_name = s
                break

        df = pd.read_excel(excel_file, sheet_name=sheet_name, engine="openpyxl")
    except Exception as e:
        logger.error(f"Falha ao ler aba principal de reposições: {e}")
        raise MissingSheetError(f"Não foi possível ler a aba de reposições: {e}")

    if df.empty:
        return _empty_repo_df()

    # Normalize column names
    col_map = {}
    for c in df.columns:
        cu = str(c).strip().upper()
        if cu == "OFICINA":
            col_map[c] = "OFICINA"
        elif cu == "MP":
            col_map[c] = "MP"
        elif "PARTE" in cu and "PE" in cu:
            col_map[c] = "PARTE_PECA"
        elif cu == "QUANTIDADE" or cu == "QTD":
            col_map[c] = "QUANTIDADE"
        elif cu == "DATA":
            col_map[c] = "DATA"
        elif cu == "STATUS":
            col_map[c] = "STATUS"
    df = df.rename(columns=col_map)

    # Ensure required columns exist
    for col in REPOSICOES_COLUMNS:
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
    df["STATUS"] = df["STATUS"].fillna("").astype(str).str.strip().str.upper()

    # Sanitize Quantity
    df["QUANTIDADE"] = pd.to_numeric(df["QUANTIDADE"], errors="coerce").fillna(1).astype(int)

    return df.reset_index(drop=True)


def _load_negadas(excel_file: pd.ExcelFile) -> pd.DataFrame:
    """Load and normalise the NEGADAS sheet (defensive fallback if missing)."""
    try:
        sheet_name = None
        for s in excel_file.sheet_names:
            if "NEGADA" in s.strip().upper():
                sheet_name = s
                break

        if sheet_name is None:
            logger.warning("Aba NEGADAS não encontrada na planilha. Retornando dataset vazio.")
            return _empty_neg_df()

        df = pd.read_excel(excel_file, sheet_name=sheet_name, engine="openpyxl")
    except Exception as e:
        logger.warning(f"Aba NEGADAS ausente ou ilegível: {e}. Retornando dataset vazio.")
        return _empty_neg_df()

    if df.empty:
        return _empty_neg_df()

    # Normalize column names
    col_map = {}
    for c in df.columns:
        cu = str(c).strip().upper()
        if cu == "TAREFA":
            col_map[c] = "TAREFA"
        elif "DATA" in cu and "CRIA" in cu:
            col_map[c] = "DATA_CRIACAO"
        elif "DESCRI" in cu:
            col_map[c] = "DESCRICAO"
    df = df.rename(columns=col_map)

    # Ensure columns exist
    if "DATA_CRIACAO" in df.columns:
        df["DATA"] = pd.to_datetime(df["DATA_CRIACAO"], errors="coerce")
        if hasattr(df["DATA"].dt, "tz") and df["DATA"].dt.tz is not None:
            df["DATA"] = df["DATA"].dt.tz_localize(None)
    else:
        df["DATA"] = pd.NaT

    if "DESCRICAO" in df.columns:
        df["QTD_EXTRAIDA"] = df["DESCRICAO"].astype(str).apply(_extract_qty)
    else:
        df["QTD_EXTRAIDA"] = 1

    if "TAREFA" in df.columns:
        df["PARTE_PECA"] = df["TAREFA"].astype(str).apply(
            lambda x: x.split(" - ")[-1].strip() if " - " in x else x.strip()
        )
    else:
        df["PARTE_PECA"] = ""

    return df.reset_index(drop=True)


def _extract_qty(text: Optional[str]) -> Optional[int]:
    """Safely extract 'Quantidade: <N>' from free text."""
    if not text or pd.isna(text):
        return None
    m = re.search(r"Quantidade:\s*(\d+)", str(text), re.IGNORECASE)
    if m:
        try:
            return int(m.group(1))
        except (ValueError, TypeError):
            return None
    return None


def _empty_repo_df() -> pd.DataFrame:
    """Returns an empty DataFrame matching the REPOSIÇÕES schema."""
    return pd.DataFrame(columns=REPOSICOES_COLUMNS)


def _empty_neg_df() -> pd.DataFrame:
    """Returns an empty DataFrame matching the NEGADAS schema."""
    return pd.DataFrame(columns=NEGADAS_COLUMNS)
