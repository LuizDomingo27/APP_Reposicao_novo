# ═══════════════════════════════════════════════════════════════════════════════
# TEST FIXTURES & DATA GENERATORS
# ═══════════════════════════════════════════════════════════════════════════════

import io
import sys
from pathlib import Path
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

    repo_data = {
        "OFICINA": ["OFICINA ALFA", "OFICINA BETA", "OFICINA ALFA", "OFICINA GAMA", "OFICINA ALFA"],
        "MP": ["ALGODÃO 100%", "POLIÉSTER", "ALGODÃO 100%", "VISCOSE", "LINHO"],
        "PARTE DA PEÇA": ["Gola", "Manga", "Gola", "Punho", "Bolso"],
        "QUANTIDADE": [2, 1, 3, 5, 2],
        "DATA": [
            "15/08/2026 10:30",
            "14/08/2026 14:20",
            "10/08/2026 09:15",
            "01/08/2026 16:45",
            "15/07/2026 11:00",
        ],
        "REPOSIÇÃO": ["COMPLETA", "INCOMPLETA", "COMPLETA", "COMPLETA", "INCOMPLETA"],
    }
    df_repo = pd.DataFrame(repo_data)

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df_repo.to_excel(writer, sheet_name="REPOSIÇÕES", index=False)

    output.seek(0)
    return output


@pytest.fixture
def sample_repo_dataframe():
    """Generates a clean DataFrame matching the Chamados schema."""
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
        "SITUACAO": ["COMPLETA", "INCOMPLETA", "COMPLETA", "INCOMPLETA"],
        "STATUS_CHAMADO": ["Finalizado", "Em Andamento", "Finalizado", "Em Andamento"],
    })
