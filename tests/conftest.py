# ═══════════════════════════════════════════════════════════════════════════════
# TEST FIXTURES & DATA GENERATORS
# ═══════════════════════════════════════════════════════════════════════════════

import io
import sys
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import pytest

# Ensure project root is in sys.path for absolute imports
ROOT_DIR = str(Path(__file__).resolve().parent.parent)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


@pytest.fixture
def sample_excel_bytes():
    """Generates an in-memory valid Excel workbook matching production structure."""
    output = io.BytesIO()
    
    # Sheet 1: REPOSIÇÕES
    repo_data = {
        "OFICINA": ["OFICINA ALFA", "OFICINA BETA", "OFICINA ALFA", "OFICINA GAMA", "OFICINA ALFA"],
        "MP": ["ALGODÃO 100%", "POLIÉSTER", "ALGODÃO 100%", "VISCOSE", "LINHO"],
        "PARTE_PECA": ["Gola", "Manga", "Gola", "Punho", "Bolso"],
        "QUANTIDADE": [2, 1, 3, 5, 2],
        "DATA": [
            "15/08/2026 10:30",
            "14/08/2026 14:20",
            "10/08/2026 09:15",
            "01/08/2026 16:45",
            "15/07/2026 11:00",
        ],
        "STATUS": ["CONCLUÍDO", "EM ANDAMENTO", "CONCLUÍDO", "CONCLUÍDO", "CANCELADO"],
    }
    df_repo = pd.DataFrame(repo_data)

    # Sheet 2: NEGADAS
    neg_data = {
        "TAREFA": ["ORD-101 - Gola", "ORD-102 - Manga", "ORD-103 - Sem Traco"],
        "DATA_CRIACAO": [
            "2026-08-15T12:00:00Z",
            "2026-08-14T15:30:00+00:00",
            "2026-07-20T10:00:00",
        ],
        "DESCRICAO": [
            "Reposição negada. Motivo: Falta de estoque. Quantidade: 4 peças.",
            "Quantidade: 2 itens avariados.",
            "Sem quantidade especificada.",
        ],
    }
    df_neg = pd.DataFrame(neg_data)

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df_repo.to_excel(writer, sheet_name="REPOSIÇÕES", index=False)
        df_neg.to_excel(writer, sheet_name="NEGADAS", index=False)

    output.seek(0)
    return output


@pytest.fixture
def sample_repo_dataframe():
    """Generates a clean DataFrame matching REPOSIÇÕES schema."""
    return pd.DataFrame({
        "OFICINA": ["OFICINA A", "OFICINA B", "OFICINA A", "OFICINA C"],
        "MP": ["TECIDO X", "TECIDO Y", "TECIDO X", "TECIDO Z"],
        "PARTE_PECA": ["Gola", "Manga", "Gola", "Bolso"],
        "QUANTIDADE": [2, 1, 4, 1],
        "DATA": [
            pd.Timestamp("2026-08-15 10:00:00"),
            pd.Timestamp("2026-08-14 11:00:00"),
            pd.Timestamp("2026-08-10 12:00:00"),
            pd.Timestamp("2026-07-05 09:00:00"),
        ],
        "STATUS": ["CONCLUÍDO", "CONCLUÍDO", "PENDENTE", "CONCLUÍDO"]
    })


@pytest.fixture
def sample_neg_dataframe():
    """Generates a clean DataFrame matching NEGADAS schema."""
    return pd.DataFrame({
        "TAREFA": ["ORD-1 - Gola", "ORD-2 - Manga"],
        "DATA_CRIACAO": ["2026-08-15T12:00:00Z", "2026-08-14T10:00:00Z"],
        "DESCRICAO": ["Quantidade: 3 peças", "Quantidade: 5 peças"],
        "DATA": [pd.Timestamp("2026-08-15 12:00:00"), pd.Timestamp("2026-08-14 10:00:00")],
        "QTD_EXTRAIDA": [3, 5],
        "PARTE_PECA": ["Gola", "Manga"]
    })
