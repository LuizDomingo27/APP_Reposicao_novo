# ═══════════════════════════════════════════════════════════════════════════════
# UNIT TESTS — Metrics, KPIs, and Aggregations
# Compatible with both Pytest and Python standard library unittest
# ═══════════════════════════════════════════════════════════════════════════════

import sys
from pathlib import Path
import unittest
import pandas as pd

# Add project root to sys.path
ROOT_DIR = str(Path(__file__).resolve().parent.parent)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from data.metrics import (
    get_chamados_kpis,
    get_status_distribution,
    get_rankings,
    get_monthly_history,
    get_weekly_distribution,
)


class TestMetrics(unittest.TestCase):
    """Test suite for KPIs, rankings, and data aggregations."""

    def setUp(self):
        self.sample_repo = pd.DataFrame({
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

    def test_get_chamados_kpis_valid(self):
        kpis = get_chamados_kpis(self.sample_repo)
        self.assertEqual(kpis["total_chamados"], 4)
        self.assertEqual(kpis["finalizados"], 2)
        self.assertEqual(kpis["em_andamento"], 2)
        self.assertEqual(kpis["taxa_finalizacao"], 50.0)
        self.assertEqual(kpis["total_pecas"], 8)
        self.assertEqual(kpis["media_pecas"], 2.0)

    def test_get_chamados_kpis_empty(self):
        empty = get_chamados_kpis(pd.DataFrame())
        self.assertEqual(empty["total_chamados"], 0)
        self.assertEqual(empty["finalizados"], 0)
        self.assertEqual(empty["taxa_finalizacao"], 0.0)

    def test_get_status_distribution(self):
        dist = get_status_distribution(self.sample_repo)
        self.assertEqual(dist["labels"], ["Finalizado", "Em Andamento"])
        self.assertEqual(dist["values"], [2, 2])
        self.assertEqual(len(dist["colors"]), 2)

    def test_get_rankings(self):
        rankings = get_rankings(self.sample_repo, top_n=3)
        self.assertGreater(len(rankings["mp_data"]), 0)
        self.assertGreater(len(rankings["parte_data"]), 0)

        top_mp = rankings["mp_data"][0]
        self.assertEqual(top_mp[0], "TECIDO X")
        self.assertEqual(top_mp[1], 2)
        self.assertEqual(top_mp[2], 50.0)

    def test_get_monthly_history(self):
        hist = get_monthly_history(self.sample_repo, n_months=3)
        self.assertEqual(len(hist["labels"]), 2)
        self.assertEqual(sum(hist["values"]), 4)

    def test_get_weekly_distribution(self):
        weekly = get_weekly_distribution(self.sample_repo, max_weeks=12)
        self.assertGreater(len(weekly["labels"]), 0)
        self.assertEqual(sum(weekly["values"]), 4)


if __name__ == "__main__":
    unittest.main()

