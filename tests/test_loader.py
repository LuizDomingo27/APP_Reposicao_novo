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
    InvalidFileError,
    REPOSICOES_COLUMNS,
    STATUS_FINALIZADO,
    STATUS_EM_ANDAMENTO,
)


class TestDataLoader(unittest.TestCase):
    """Test suite for data loading and Excel validation."""

    def _create_sample_excel(self) -> io.BytesIO:
        output = io.BytesIO()
        df_repo = pd.DataFrame({
            "OFICINA": ["OFICINA ALFA", "OFICINA BETA", "OFICINA ALFA"],
            "MP": ["ALGODÃO 100%", "POLIÉSTER", "ALGODÃO 100%"],
            "PARTE DA PEÇA": ["Gola", "Manga", "Gola"],
            "QUANTIDADE": [2, 1, 99999999],  # last is an outlier / data-entry error
            "DATA": ["15/08/2026 10:30", "14/08/2026 14:20", "10/08/2026 09:15"],
            "REPOSIÇÃO": ["COMPLETA", "INCOMPLETA", ""],  # blank => Em Andamento
        })
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df_repo.to_excel(writer, sheet_name="REPOSIÇÕES", index=False)
        output.seek(0)
        return output

    def test_load_data_valid_excel(self):
        df_repo = load_data(self._create_sample_excel())

        self.assertFalse(df_repo.empty)
        for col in REPOSICOES_COLUMNS:
            self.assertIn(col, df_repo.columns)

        # Timezone normalization
        self.assertIsNone(df_repo["DATA"].dt.tz)

    def test_status_chamado_derivation(self):
        df_repo = load_data(self._create_sample_excel())
        # COMPLETA + INCOMPLETA -> Finalizado; blank -> Em Andamento
        self.assertEqual((df_repo["STATUS_CHAMADO"] == STATUS_FINALIZADO).sum(), 2)
        self.assertEqual((df_repo["STATUS_CHAMADO"] == STATUS_EM_ANDAMENTO).sum(), 1)

    def test_quantidade_outliers_stripped(self):
        df_repo = load_data(self._create_sample_excel())
        # The 99.999.999 value must be dropped to NaN, leaving only 2 + 1 = 3 pieces
        self.assertEqual(int(df_repo["QUANTIDADE"].sum()), 3)
        self.assertEqual(df_repo["QUANTIDADE"].isna().sum(), 1)

    def test_load_data_none_file(self):
        df_repo = load_data(None)
        self.assertTrue(df_repo.empty)
        for col in REPOSICOES_COLUMNS:
            self.assertIn(col, df_repo.columns)

    def test_load_data_invalid_bytes(self):
        corrupted = io.BytesIO(b"this is not an excel file")
        with self.assertRaises(InvalidFileError):
            load_data(corrupted)


if __name__ == "__main__":
    unittest.main()
