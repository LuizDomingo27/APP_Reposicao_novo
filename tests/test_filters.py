# ═══════════════════════════════════════════════════════════════════════════════
# UNIT TESTS — Data Filters & Period Logic (Date Range + Legacy Period)
# Compatible with both Pytest and Python standard library unittest
# ═══════════════════════════════════════════════════════════════════════════════

import sys
from pathlib import Path
from datetime import datetime, date
import unittest
import pandas as pd

# Add project root to sys.path
ROOT_DIR = str(Path(__file__).resolve().parent.parent)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from data.filters import (
    filter_by_period,
    filter_by_date_range,
    get_period_label,
    get_date_range_label,
    _resolve_ref_date,
)


class TestDataFilters(unittest.TestCase):
    """Test suite for date filtering and timezone resolution."""

    def setUp(self):
        self.sample_df = pd.DataFrame({
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

    # ── filter_by_period (legacy preset tests) ─────────────────────────────

    def test_filter_by_period_day(self):
        ref_date = date(2026, 8, 15)
        filtered = filter_by_period(self.sample_df, col="DATA", period="Dia", ref_date=ref_date)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered.iloc[0]["OFICINA"], "OFICINA A")

    def test_filter_by_period_week(self):
        ref_date = date(2026, 8, 15)
        filtered = filter_by_period(self.sample_df, col="DATA", period="Semana", ref_date=ref_date)
        self.assertEqual(len(filtered), 3)

    def test_filter_by_period_month(self):
        ref_date = date(2026, 8, 15)
        filtered = filter_by_period(self.sample_df, col="DATA", period="Mês", ref_date=ref_date)
        self.assertEqual(len(filtered), 3)

    def test_filter_by_period_empty_or_none(self):
        self.assertTrue(filter_by_period(None).empty)
        self.assertTrue(filter_by_period(pd.DataFrame()).empty)

    def test_filter_by_period_timezone_aware(self):
        df_tz = pd.DataFrame({
            "DATA": pd.to_datetime(["2026-08-15T12:00:00Z", "2026-08-01T10:00:00Z"])
        })
        filtered = filter_by_period(df_tz, col="DATA", period="Dia", ref_date=date(2026, 8, 15))
        self.assertEqual(len(filtered), 1)

    def test_get_period_label(self):
        ref = date(2026, 8, 15)
        self.assertEqual(get_period_label("Dia", ref), "15/08/2026")
        self.assertIn("08/2026", get_period_label("Mês", ref))
        self.assertIn("à", get_period_label("Semana", ref))

    # ── filter_by_date_range (new dynamic interval tests) ──────────────────

    def test_date_range_exact_interval(self):
        """Filter with explicit start and end dates."""
        filtered = filter_by_date_range(
            self.sample_df, col="DATA",
            start_date=date(2026, 8, 10),
            end_date=date(2026, 8, 15),
        )
        self.assertEqual(len(filtered), 3)

    def test_date_range_single_day(self):
        """When start == end, behaves like a day filter."""
        filtered = filter_by_date_range(
            self.sample_df, col="DATA",
            start_date=date(2026, 8, 15),
            end_date=date(2026, 8, 15),
        )
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered.iloc[0]["OFICINA"], "OFICINA A")

    def test_date_range_open_start(self):
        """Only end_date provided — returns everything up to that date."""
        filtered = filter_by_date_range(
            self.sample_df, col="DATA",
            start_date=None,
            end_date=date(2026, 8, 10),
        )
        self.assertEqual(len(filtered), 2)  # Aug 10 + Jul 5

    def test_date_range_open_end(self):
        """Only start_date provided — returns everything from that date on."""
        filtered = filter_by_date_range(
            self.sample_df, col="DATA",
            start_date=date(2026, 8, 14),
            end_date=None,
        )
        self.assertEqual(len(filtered), 2)  # Aug 14 + Aug 15

    def test_date_range_no_dates_returns_all(self):
        """Both None — returns all data unchanged."""
        filtered = filter_by_date_range(
            self.sample_df, col="DATA",
            start_date=None,
            end_date=None,
        )
        self.assertEqual(len(filtered), 4)

    def test_date_range_no_match(self):
        """Range that matches nothing returns empty DataFrame."""
        filtered = filter_by_date_range(
            self.sample_df, col="DATA",
            start_date=date(2025, 1, 1),
            end_date=date(2025, 1, 31),
        )
        self.assertEqual(len(filtered), 0)

    def test_date_range_empty_or_none_df(self):
        """Edge cases: None or empty DataFrame."""
        self.assertTrue(filter_by_date_range(None, start_date=date(2026, 1, 1)).empty)
        self.assertTrue(filter_by_date_range(pd.DataFrame(), start_date=date(2026, 1, 1)).empty)

    def test_date_range_timezone_aware(self):
        """Timezone-aware columns are handled correctly."""
        df_tz = pd.DataFrame({
            "DATA": pd.to_datetime(["2026-08-15T12:00:00Z", "2026-08-01T10:00:00Z"])
        })
        filtered = filter_by_date_range(
            df_tz, col="DATA",
            start_date=date(2026, 8, 15),
            end_date=date(2026, 8, 15),
        )
        self.assertEqual(len(filtered), 1)

    def test_date_range_cross_month(self):
        """Range spanning multiple months."""
        filtered = filter_by_date_range(
            self.sample_df, col="DATA",
            start_date=date(2026, 7, 1),
            end_date=date(2026, 8, 15),
        )
        self.assertEqual(len(filtered), 4)

    # ── get_date_range_label ───────────────────────────────────────────────

    def test_date_range_label_full_interval(self):
        label = get_date_range_label(date(2026, 8, 1), date(2026, 8, 15))
        self.assertEqual(label, "01/08/2026 à 15/08/2026")

    def test_date_range_label_single_day(self):
        label = get_date_range_label(date(2026, 8, 15), date(2026, 8, 15))
        self.assertEqual(label, "15/08/2026")

    def test_date_range_label_open_start(self):
        label = get_date_range_label(None, date(2026, 8, 15))
        self.assertIn("Até", label)
        self.assertIn("15/08/2026", label)

    def test_date_range_label_open_end(self):
        label = get_date_range_label(date(2026, 8, 1), None)
        self.assertIn("A partir de", label)
        self.assertIn("01/08/2026", label)

    def test_date_range_label_no_dates(self):
        label = get_date_range_label(None, None)
        self.assertEqual(label, "Todo o Período")


if __name__ == "__main__":
    unittest.main()
