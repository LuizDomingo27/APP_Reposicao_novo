# ═══════════════════════════════════════════════════════════════════════════════
# COMPONENT: CHARTS — Chart.js modern & minimalist interactive charts
# ═══════════════════════════════════════════════════════════════════════════════

import json
from typing import List
from config.tokens import COLORS, FONT_FAMILY, FONT_CDN, CHARTJS_CDN, DONUT_COLORS
from config.icons import get_svg_icon


def build_donut_chart_html(
    labels: List[str],
    values: List[int],
    colors: List[str] = None,
    title: str = "Proporção - Últimos 3 Meses",
    center_label: str = "Total Geral",
) -> str:
    """
    Generates standalone HTML/JS for a Donut Chart with a central total metric.
    Uses Chart.js and contains zero emojis.
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
                <span>{title}</span>
            </div>
            <div class="chart-wrapper">
                <canvas id="donutChart"></canvas>
                <div class="center-metric">
                    <div class="center-value">{total:,}</div>
                    <div class="center-label">{center_label}</div>
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


def build_area_chart_html(
    labels: List[str],
    values: List[int],
    title: str = "Chamados por Semana",
    subtitle: str = "Evolução semanal do volume de chamados",
    icon_name: str = "trending_up",
    line_color: str = COLORS["green_accent"],
    fill_color: str = "rgba(45, 138, 78, 0.18)",
    border_accent_color: str = COLORS["green_accent"],
    chart_id: str = "areaChart",
    height: int = 340,
    dataset_label: str = "Chamados",
) -> str:
    """
    Generates standalone HTML/JS for a smooth area/line chart (reference style):
    soft gradient fill, curved line, dashed horizontal grid and hidden vertical grid.
    """
    labels_json = json.dumps(labels)
    values_json = json.dumps(values)
    icon_line = get_svg_icon(icon_name, size=16, color=border_accent_color)

    header = f"""
                <div class="card-title">
                    {icon_line}
                    <span>{title}</span>
                </div>
                <div class="card-subtitle">{subtitle}</div>
    """

    base_style = f"""
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
                display: flex;
                align-items: center;
                gap: 8px;
            }}
            .card-subtitle {{
                font-size: 0.78rem;
                color: {COLORS['text_secondary']};
                font-weight: 500;
                margin-top: 4px;
                margin-bottom: 14px;
                padding-bottom: 10px;
                border-bottom: 2px solid {border_accent_color};
            }}
            .chart-wrapper {{ width: 100%; height: {height}px; }}
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
    """

    if not labels or not values or sum(values) == 0:
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <link href="{FONT_CDN}" rel="stylesheet">
            <style>{base_style}</style>
        </head>
        <body>
            <div class="card">
                {header}
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
        <style>{base_style}</style>
    </head>
    <body>
        <div class="card">
            {header}
            <div class="chart-wrapper">
                <canvas id="{chart_id}"></canvas>
            </div>
        </div>
        <script>
        (function() {{
            const ctx = document.getElementById('{chart_id}').getContext('2d');

            const pointDataLabelsPlugin = {{
                id: 'pointDataLabels',
                afterDatasetsDraw(chart) {{
                    const {{ ctx, data }} = chart;
                    ctx.save();
                    ctx.font = "bold 10px 'Outfit', sans-serif";
                    ctx.fillStyle = '{COLORS['text_primary']}';
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'bottom';
                    chart.getDatasetMeta(0).data.forEach((pt, i) => {{
                        const val = data.datasets[0].data[i];
                        if (val !== undefined && val !== null) {{
                            ctx.fillText(val.toLocaleString('pt-BR'), pt.x, pt.y - 7);
                        }}
                    }});
                    ctx.restore();
                }}
            }};

            new Chart(ctx, {{
                type: 'line',
                data: {{
                    labels: {labels_json},
                    datasets: [{{
                        label: '{dataset_label}',
                        data: {values_json},
                        borderColor: '{line_color}',
                        borderWidth: 2.5,
                        tension: 0.4,
                        pointRadius: 2,
                        pointBackgroundColor: '{line_color}',
                        pointHoverRadius: 5,
                        pointHoverBackgroundColor: '{line_color}',
                        pointHoverBorderColor: '#FFFFFF',
                        pointHoverBorderWidth: 2,
                        fill: true,
                        backgroundColor: function(context) {{
                            const chart = context.chart;
                            const {{ctx: c, chartArea}} = chart;
                            if (!chartArea) return '{fill_color}';
                            const gradient = c.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
                            gradient.addColorStop(0, '{fill_color}');
                            gradient.addColorStop(1, 'rgba(255,255,255,0)');
                            return gradient;
                        }}
                    }}]
                }},
                plugins: [pointDataLabelsPlugin],
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: {{ mode: 'index', intersect: false }},
                    layout: {{ padding: {{ top: 26, bottom: 4, left: 6, right: 12 }} }},
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
                                maxRotation: 0,
                                autoSkip: true,
                                padding: 6
                            }},
                            border: {{ display: true, color: '{COLORS['border_card']}' }}
                        }},
                        y: {{
                            beginAtZero: true,
                            display: false,
                            grid: {{ display: false }},
                            ticks: {{ display: false }},
                            border: {{ display: false }},
                            grace: '18%'
                        }}
                    }},
                    animation: {{ duration: 900, easing: 'easeOutQuart' }}
                }}
            }});
        }})();
        </script>
    </body>
    </html>
    """

