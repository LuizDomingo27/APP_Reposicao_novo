# ═══════════════════════════════════════════════════════════════════════════════
# UNIT TESTS — Components, Charts & Vector Icons
# Compatible with both Pytest and Python standard library unittest
# ═══════════════════════════════════════════════════════════════════════════════

import re
import sys
from pathlib import Path
import unittest

# Add project root to sys.path
ROOT_DIR = str(Path(__file__).resolve().parent.parent)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from config.icons import get_svg_icon
from components.charts import build_donut_chart_html, build_bar_chart_html


class TestComponents(unittest.TestCase):
    """Test suite for SVG icons and component generators."""

    def test_get_svg_icon_valid_base64_tag(self):
        for icon_name in ["logo", "upload", "calendar", "chart_bar", "chart_pie", "table"]:
            tag = get_svg_icon(icon_name, size=24, color="#E8762D")
            self.assertTrue(tag.startswith('<img src="data:image/svg+xml;base64,'))
            self.assertIn(f'alt="{icon_name}"', tag)

    def test_no_emojis_in_charts(self):
        donut_html = build_donut_chart_html(labels=["Ago/2026", "Jul/2026"], values=[10, 5])
        bar_html = build_bar_chart_html(labels=["S32", "S33"], values=[15, 20])

        emoji_pattern = re.compile(
            r"[\U00010000-\U0010ffff]|[\u2600-\u27bf]|[\u2300-\u23ff]|[\u2b50-\u2b55]"
        )

        self.assertIsNone(emoji_pattern.search(donut_html), "Emoji found in donut chart HTML!")
        self.assertIsNone(emoji_pattern.search(bar_html), "Emoji found in bar chart HTML!")

    def test_bar_chart_datalabels_and_hidden_y_axis(self):
        bar_html = build_bar_chart_html(labels=["S32", "S33"], values=[15, 20])
        self.assertIn("topDataLabels", bar_html)
        self.assertIn("display: false", bar_html)


if __name__ == "__main__":
    unittest.main()
