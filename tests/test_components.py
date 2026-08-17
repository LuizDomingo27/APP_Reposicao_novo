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
from components.charts import build_donut_chart_html, build_area_chart_html


class TestComponents(unittest.TestCase):
    """Test suite for SVG icons and component generators."""

    def test_get_svg_icon_valid_base64_tag(self):
        for icon_name in ["logo", "upload", "calendar", "chart_bar", "chart_pie", "table",
                          "check_circle", "clock", "clipboard", "trending_up"]:
            tag = get_svg_icon(icon_name, size=24, color="#E8762D")
            self.assertTrue(tag.startswith('<img src="data:image/svg+xml;base64,'))
            self.assertIn(f'alt="{icon_name}"', tag)

    def test_no_emojis_in_charts(self):
        donut_html = build_donut_chart_html(labels=["Finalizado", "Em Andamento"], values=[10, 5])
        area_html = build_area_chart_html(labels=["S32", "S33"], values=[15, 20])

        emoji_pattern = re.compile(
            r"[\U00010000-\U0010ffff]|[\u2600-\u27bf]|[\u2300-\u23ff]|[\u2b50-\u2b55]"
        )

        self.assertIsNone(emoji_pattern.search(donut_html), "Emoji found in donut chart HTML!")
        self.assertIsNone(emoji_pattern.search(area_html), "Emoji found in area chart HTML!")

    def test_area_chart_line_type_and_empty_state(self):
        area_html = build_area_chart_html(labels=["S32", "S33"], values=[15, 20])
        self.assertIn("type: 'line'", area_html)
        self.assertIn("Chamados por Semana", area_html)

        empty_html = build_area_chart_html(labels=[], values=[])
        self.assertIn("Nenhum dado registrado", empty_html)

    def test_donut_custom_title_and_center(self):
        html = build_donut_chart_html(
            labels=["Finalizado", "Em Andamento"], values=[10, 5],
            title="Status dos Chamados", center_label="Total",
        )
        self.assertIn("Status dos Chamados", html)
        self.assertIn("Total", html)


if __name__ == "__main__":
    unittest.main()
