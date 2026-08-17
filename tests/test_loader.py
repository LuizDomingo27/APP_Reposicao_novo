# ═══════════════════════════════════════════════════════════════════════════════
# UNIT TESTS — Data Loader & Excel Ingestion
# Compatible with both Pytest and Python standard library unittest
# ═══════════════════════════════════════════════════════════════════════════════

import io
import sys
from pathlib import Path
import unittest
import pandas as pd

# Add project root to sys.path
ROOT_DIR = str(Path(__file__).resolve().parent.parent)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from data.loader import (
    load_data,
    _load_reposicoes,
    _load_negadas,
    _extract_qty,
    InvalidFileError,
    REPOSICOES_COLUMNS,
    NEGADAS_COLUMNS,
)


class TestDataLoader(unittest.TestCase):
    """Test suite for data loading and Excel validation."""

    def _create_sample_excel(self) -> io.BytesIO:
        output = io.BytesIO()
        df_repo = pd.DataFrame({
            "OFICINA": ["OFICINA ALFA", "OFICINA BETA", "OFICINA ALFA"],
            "MP": ["ALGODÃO 100%", "POLIÉSTER", "ALGODÃO 100%"],
            "PARTE_PECA": ["Gola", "Manga", "Gola"],
            "QUANTIDADE": [2, 1, 3],
            "DATA": ["15/08/2026 10:30", "14/08/2026 14:20", "10/08/2026 09:15"],
            "STATUS": ["CONCLUÍDO", "EM ANDAMENTO", "CONCLUÍDO"],
        })
        df_neg = pd.DataFrame({
            "TAREFA": ["ORD-101 - Gola", "ORD-102 - Manga"],
            "DATA_CRIACAO": ["2026-08-15T12:00:00Z", "2026-08-14T15:30:00+00:00"],
            "DESCRICAO": ["Quantidade: 4 peças.", "Quantidade: 2 itens."],
        })
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df_repo.to_excel(writer, sheet_name="REPOSIÇÕES", index=False)
            df_neg.to_excel(writer, sheet_name="NEGADAS", index=False)
        output.seek(0)
        return output

    def test_load_data_valid_excel(self):
        excel_file = self._create_sample_excel()
        df_repo, df_neg = load_data(excel_file)

        self.assertFalse(df_repo.empty)
        self.assertFalse(df_neg.empty)
        for col in REPOSICOES_COLUMNS:
            self.assertIn(col, df_repo.columns)
        for col in NEGADAS_COLUMNS:
            self.assertIn(col, df_neg.columns)

        # Check timezone normalization
        self.assertIsNone(df_repo["DATA"].dt.tz)
        self.assertIsNone(df_neg["DATA"].dt.tz)

    def test_load_data_none_file(self):
        df_repo, df_neg = load_data(None)
        self.assertTrue(df_repo.empty)
        self.assertTrue(df_neg.empty)

    def test_load_data_invalid_bytes(self):
        corrupted = io.BytesIO(b"this is not an excel file")
        with self.assertRaises(InvalidFileError):
            load_data(corrupted)

    def test_load_data_missing_negadas_sheet(self):
        output = io.BytesIO()
        df = pd.DataFrame({
            "OFICINA": ["OFICINA A"],
            "DATA": ["15/08/2026 10:00"],
            "QUANTIDADE": [1]
        })
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="REPOSIÇÕES", index=False)
        output.seek(0)

        df_repo, df_neg = load_data(output)
        self.assertFalse(df_repo.empty)
        self.assertTrue(df_neg.empty)
        for col in NEGADAS_COLUMNS:
            self.assertIn(col, df_neg.columns)

    def test_extract_qty_regex(self):
        self.assertEqual(_extract_qty("Quantidade: 5 peças solicitadas"), 5)
        self.assertEqual(_extract_qty("quantidade:10"), 10)
        self.assertEqual(_extract_qty("QUANTIDADE: 120 itens"), 120)
        self.assertIsNone(_extract_qty("Sem quantidade informada"))
        self.assertIsNone(_extract_qty(""))
        self.assertIsNone(_extract_qty(None))


if __name__ == "__main__":
    unittest.main()
