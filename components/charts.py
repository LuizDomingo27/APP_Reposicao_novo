# ═══════════════════════════════════════════════════════════════════════════════
# COMPONENT: CHARTS — Chart.js modern & minimalist interactive charts
# ═══════════════════════════════════════════════════════════════════════════════

import json
from typing import List
from config.tokens import COLORS, FONT_FAMILY, FONT_CDN, CHARTJS_CDN, DONUT_COLORS
from config.icons import get_svg_icon


def build_donut_chart_html(labels: List[str], values: List[int], colors: List[str] = None) -> str:
    """
    Generates standalone HTML/JS for Donut Chart showing last 3 months.
    Uses Chart.js with central total metric and zero emojis.
    """
    if colors is None:
        colors = DONUT_COLORS[:len(values)]

    total = sum(values)
    labels_json = json.dumps(labels)
    values_json = json.dumps(values)
    colors_json = json.dumps(colors)
    icon_pie = get_svg_icon("chart_pie", size=16, color=COLORS["orange"])

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <link href="{FONT_CDN}" rel="stylesheet">
        <script src="{CHARTJS_CDN}"></script>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            html, body {{
                font-family: {FONT_FAMILY};
                background: transparent;
                overflow: hidden;
            }}
            .card {{
                background: {COLORS['bg_card']};
                border-radius: 16px;
                padding: 22px 26px;
                border: 1px solid {COLORS['border_card']};
                box-shadow: 0 2px 12px rgba(0,0,0,0.03);
            }}
            .card-title {{
                font-size: 0.75rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                color: {COLORS['text_primary']};
                margin-bottom: 14px;
                padding-bottom: 10px;
                border-bottom: 2px solid {COLORS['orange']};
                display: flex;
                align-items: center;
                gap: 8px;
            }}
            .chart-wrapper {{
                position: relative;
                width: 100%;
                max-width: 290px;
                margin: 0 auto;
                height: 290px;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            .center-metric {{
                position: absolute;
                top: 42%;
                left: 50%;
                transform: translate(-50%, -50%);
                text-align: center;
                pointer-events: none;
            }}
            .center-value {{
                font-size: 1.8rem;
                font-weight: 800;
                color: {COLORS['text_primary']};
                line-height: 1;
                letter-spacing: -0.02em;
            }}
            .center-label {{
                font-size: 0.68rem;
                color: {COLORS['text_secondary']};
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 0.06em;
                margin-top: 3px;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="card-title">
                {icon_pie}
                <span>Proporção - Últimos 3 Meses</span>
            </div>
            <div class="chart-wrapper">
                <canvas id="donutChart"></canvas>
                <div class="center-metric">
                    <div class="center-value">{total:,}</div>
                    <div class="center-label">Total Geral</div>
                </div>
            </div>
        </div>
        <script>
        (function() {{
            const ctx = document.getElementById('donutChart').getContext('2d');
            const total = {total};
            new Chart(ctx, {{
                type: 'doughnut',
                data: {{
                    labels: {labels_json},
                    datasets: [{{
                        data: {values_json},
                        backgroundColor: {colors_json},
                        borderWidth: 0,
                        borderRadius: 5,
                        spacing: 3,
                        hoverOffset: 6,
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: '70%',
                    plugins: {{
                        legend: {{
                            position: 'bottom',
                            labels: {{
                                font: {{ family: "'Outfit', sans-serif", size: 11, weight: '600' }},
                                color: '{COLORS['text_primary']}',
                                padding: 12,
                                usePointStyle: true,
                                pointStyleWidth: 10,
                                generateLabels: function(chart) {{
                                    const data = chart.data;
                                    return data.labels.map((label, i) => {{
                                        const value = data.datasets[0].data[i];
                                        const pct = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
                                        return {{
                                            text: label + ' — ' + value.toLocaleString('pt-BR') + ' (' + pct + '%)',
                                            fillStyle: data.datasets[0].backgroundColor[i],
                                            strokeStyle: 'transparent',
                                            lineWidth: 0,
                                            pointStyle: 'rectRounded',
                                            index: i,
                                        }};
                                    }});
                                }}
                            }}
                        }},
                        tooltip: {{
                            backgroundColor: '{COLORS['text_primary']}',
                            titleFont: {{ family: "'Outfit', sans-serif", size: 12, weight: '600' }},
                            bodyFont: {{ family: "'Outfit', sans-serif", size: 11 }},
                            cornerRadius: 8,
                            padding: 10,
                            callbacks: {{
                                label: function(ctx) {{
                                    const pct = total > 0 ? ((ctx.parsed / total) * 100).toFixed(1) : 0;
                                    return ctx.label + ': ' + ctx.parsed.toLocaleString('pt-BR') + ' (' + pct + '%)';
                                }}
                            }}
                        }}
                    }},
                    animation: {{
                        animateRotate: true,
                        duration: 1000,
                        easing: 'easeOutQuart'
                    }}
                }}
            }});
        }})();
        </script>
    </body>
    </html>
    """


def build_bar_chart_html(
    labels: List[str],
    values: List[int],
    title: str = "Distribuição Semanal (Últimas Semanas)",
    icon_name: str = "chart_bar",
    color_start: str = COLORS["green_light"],
    color_end: str = COLORS["green_accent"],
    border_accent_color: str = COLORS["green_light"],
    chart_id: str = "barChart",
    height: int = 380,
    dataset_label: str = "Total"
) -> str:
    """
    Generates standalone HTML/JS for Bar/Column Chart with data labels on top of bars,
    Y-axis values and horizontal grid lines removed, and smooth animations.
    """
    labels_json = json.dumps(labels)
    values_json = json.dumps(values)
    icon_bar = get_svg_icon(icon_name, size=16, color=color_end)

    if not labels or not values or sum(values) == 0:
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <link href="{FONT_CDN}" rel="stylesheet">
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                html, body {{
                    font-family: {FONT_FAMILY};
                    background: transparent;
                    overflow: hidden;
                }}
                .card {{
                    background: {COLORS['bg_card']};
                    border-radius: 16px;
                    padding: 22px 26px;
                    border: 1px solid {COLORS['border_card']};
                    box-shadow: 0 2px 12px rgba(0,0,0,0.03);
                }}
                .card-title {{
                    font-size: 0.75rem;
                    font-weight: 700;
                    text-transform: uppercase;
                    letter-spacing: 0.08em;
                    color: {COLORS['text_primary']};
                    margin-bottom: 14px;
                    padding-bottom: 10px;
                    border-bottom: 2px solid {border_accent_color};
                    display: flex;
                    align-items: center;
                    gap: 8px;
                }}
                .empty-wrapper {{
                    width: 100%;
                    height: {height}px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: {COLORS['text_secondary']};
                    font-size: 0.85rem;
                    font-weight: 500;
                }}
            </style>
        </head>
        <body>
            <div class="card">
                <div class="card-title">
                    {icon_bar}
                    <span>{title}</span>
                </div>
                <div class="empty-wrapper">
                    Nenhum dado registrado para o período selecionado.
                </div>
            </div>
        </body>
        </html>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <link href="{FONT_CDN}" rel="stylesheet">
        <script src="{CHARTJS_CDN}"></script>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            html, body {{
                font-family: {FONT_FAMILY};
                background: transparent;
                overflow: hidden;
            }}
            .card {{
                background: {COLORS['bg_card']};
                border-radius: 16px;
                padding: 22px 26px;
                border: 1px solid {COLORS['border_card']};
                box-shadow: 0 2px 12px rgba(0,0,0,0.03);
            }}
            .card-title {{
                font-size: 0.75rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                color: {COLORS['text_primary']};
                margin-bottom: 14px;
                padding-bottom: 10px;
                border-bottom: 2px solid {border_accent_color};
                display: flex;
                align-items: center;
                gap: 8px;
            }}
            .chart-wrapper {{
                width: 100%;
                height: {height}px;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="card-title">
                {icon_bar}
                <span>{title}</span>
            </div>
            <div class="chart-wrapper">
                <canvas id="{chart_id}"></canvas>
            </div>
        </div>
        <script>
        (function() {{
            const ctx = document.getElementById('{chart_id}').getContext('2d');
            const dataValues = {values_json};
            const hasData = dataValues && dataValues.length > 0 && Math.max(...dataValues, 0) > 0;

            const topDataLabelsPlugin = {{
                id: 'topDataLabels',
                afterDatasetsDraw(chart) {{
                    const {{ ctx, data }} = chart;
                    ctx.save();
                    ctx.font = "bold 11px 'Outfit', sans-serif";
                    ctx.fillStyle = '{COLORS['text_primary']}';
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'bottom';
                    chart.getDatasetMeta(0).data.forEach((bar, index) => {{
                        const val = data.datasets[0].data[index];
                        if (val !== undefined && val !== null && val > 0) {{
                            ctx.fillText(val.toLocaleString('pt-BR'), bar.x, bar.y - 4);
                        }}
                    }});
                    ctx.restore();
                }}
            }};

            new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: {labels_json},
                    datasets: [{{
                        label: '{dataset_label}',
                        data: {values_json},
                        backgroundColor: function(context) {{
                            const chart = context.chart;
                            const {{ctx: c, chartArea}} = chart;
                            if (!chartArea) return '{color_start}';
                            const gradient = c.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
                            gradient.addColorStop(0, '{color_start}');
                            gradient.addColorStop(1, '{color_end}');
                            return gradient;
                        }},
                        borderRadius: {{ topLeft: 6, topRight: 6 }},
                        borderSkipped: false,
                        barPercentage: 0.65,
                        categoryPercentage: 0.8
                    }}]
                }},
                plugins: [topDataLabelsPlugin],
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    layout: {{
                        padding: {{
                            top: 24,
                            bottom: 5,
                            left: 5,
                            right: 5
                        }}
                    }},
                    plugins: {{
                        legend: {{ display: false }},
                        tooltip: {{
                            backgroundColor: '{COLORS['text_primary']}',
                            titleFont: {{ family: "'Outfit', sans-serif", size: 12, weight: '600' }},
                            bodyFont: {{ family: "'Outfit', sans-serif", size: 11 }},
                            cornerRadius: 8,
                            padding: 10,
                            callbacks: {{
                                label: function(ctx) {{
                                    return '{dataset_label}: ' + ctx.parsed.y.toLocaleString('pt-BR');
                                }}
                            }}
                        }}
                    }},
                    scales: {{
                        x: {{
                            grid: {{ display: false }},
                            ticks: {{
                                font: {{ family: "'Outfit', sans-serif", size: 11, weight: '500' }},
                                color: '{COLORS['text_secondary']}',
                                padding: 6
                            }},
                            border: {{ display: true, color: '{COLORS['border_card']}' }}
                        }},
                        y: {{
                            display: false,
                            grid: {{ display: false }},
                            ticks: {{ display: false }},
                            border: {{ display: false }},
                            grace: '15%'
                        }}
                    }},
                    animation: {{
                        duration: 900,
                        easing: 'easeOutQuart'
                    }}
                }}
            }});
        }})();
        </script>
    </body>
    </html>
    """

