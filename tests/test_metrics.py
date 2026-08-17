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
    get_kpis,
    get_rankings,
    get_negadas_metrics,
    get_negadas_distribution,
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
            "STATUS": ["CONCLUÍDO", "CONCLUÍDO", "PENDENTE", "CONCLUÍDO"]
        })

        self.sample_neg = pd.DataFrame({
            "TAREFA": ["ORD-1 - Gola", "ORD-2 - Manga"],
            "DATA_CRIACAO": ["2026-08-15T12:00:00Z", "2026-08-14T10:00:00Z"],
            "DESCRICAO": ["Quantidade: 3 peças", "Quantidade: 5 peças"],
            "DATA": [pd.Timestamp("2026-08-15 12:00:00"), pd.Timestamp("2026-08-14 10:00:00")],
            "QTD_EXTRAIDA": [3, 5],
            "PARTE_PECA": ["Gola", "Manga"]
        })

    def test_get_kpis_valid(self):
        kpis = get_kpis(self.sample_repo)
        self.assertEqual(kpis["total_repo"], 4)
        self.assertEqual(kpis["top_oficina"], "Oficina A")
        self.assertEqual(kpis["top_oficina_count"], 2)

    def test_get_kpis_empty(self):
        empty_kpi = get_kpis(pd.DataFrame())
        self.assertEqual(empty_kpi["total_repo"], 0)
        self.assertEqual(empty_kpi["top_oficina"], "N/A")
        self.assertEqual(empty_kpi["top_oficina_count"], 0)

    def test_get_rankings(self):
        rankings = get_rankings(self.sample_repo, top_n=3)
        self.assertGreater(len(rankings["mp_data"]), 0)
        self.assertGreater(len(rankings["parte_data"]), 0)

        top_mp = rankings["mp_data"][0]
        self.assertEqual(top_mp[0], "TECIDO X")
        self.assertEqual(top_mp[1], 2)
        self.assertEqual(top_mp[2], 50.0)

    def test_get_negadas_metrics(self):
        neg_metrics = get_negadas_metrics(self.sample_neg)
        self.assertEqual(neg_metrics["total_negadas"], 2)
        self.assertEqual(neg_metrics["total_pecas"], 8)
        self.assertEqual(neg_metrics["media_pecas"], 4.0)

    def test_get_negadas_distribution(self):
        dist = get_negadas_distribution(self.sample_neg, max_weeks=12)
        self.assertGreater(len(dist["weekly_negadas_labels"]), 0)
        self.assertEqual(sum(dist["weekly_negadas_values"]), 2)
        self.assertEqual(sum(dist["weekly_pecas_values"]), 8)

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

