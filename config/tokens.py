# ═══════════════════════════════════════════════════════════════════════════════
# DESIGN TOKENS — Single source of truth for all visual constants
# ═══════════════════════════════════════════════════════════════════════════════

# Palette
COLORS = {
    "bg_primary":     "#FAF6F0",
    "bg_secondary":   "#F0EBE3",
    "bg_card":        "white",
    "border_card":    "#E8E4DE",
    "green_dark":     "#1B3A2D",
    "green_mid":      "#2D5A42",
    "green_light":    "#5DB55B",
    "green_accent":   "#2D8A4E",
    "orange":         "#E8762D",
    "orange_warm":    "#FFB74D",
    "red_dark":       "#8B1A1A",
    "red_mid":        "#A52A2A",
    "red_light":      "#C0392B",
    "text_primary":   "#1B3A2D",
    "text_secondary": "#6B7B6E",
    "text_muted":     "#999",
    "bar_track":      "#E8E4DE",
}

# Typography
FONT_FAMILY = "'Outfit', sans-serif"
FONT_CDN = "https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap"

# Chart.js CDN
CHARTJS_CDN = "https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js"

# Spacing & Radii
RADIUS_CARD = "16px"
RADIUS_PILL = "20px"
RADIUS_SMALL = "8px"
GAP = "20px"
SHADOW_CARD = "0 2px 12px rgba(0,0,0,0.04)"
SHADOW_ELEVATED = "0 8px 32px rgba(27,58,45,0.18)"

# Month names (pt-BR)
MESES_PT = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro",
}

# Donut chart color sequence
DONUT_COLORS = ["#E8762D", "#5DB55B", "#1B3A2D", "#FFB74D"]

# ─── Light KPI Card Tints (reference dashboard style) ───────────────────────────
# Each tint: soft background, matching icon chip background, and a saturated
# foreground used for the icon stroke and (optionally) the metric value.
CARD_TINTS = {
    "blue":   {"bg": "#EFF5FF", "border": "#DCE8FB", "icon_bg": "#DCE8FB", "fg": "#2563EB"},
    "green":  {"bg": "#ECF7F0", "border": "#D4EDDD", "icon_bg": "#D4EDDD", "fg": "#1F9D57"},
    "amber":  {"bg": "#FEF6EC", "border": "#FBE6CC", "icon_bg": "#FBE6CC", "fg": "#E8762D"},
    "indigo": {"bg": "#F2F1FC", "border": "#E2E0F6", "icon_bg": "#E2E0F6", "fg": "#5B54C9"},
    "teal":   {"bg": "#EAF7F5", "border": "#D2ECE9", "icon_bg": "#D2ECE9", "fg": "#0E9E96"},
    "slate":  {"bg": "#F4F6F8", "border": "#E4E8ED", "icon_bg": "#E4E8ED", "fg": "#5B6B7B"},
}

# Status donut colors (Chamados)
STATUS_COLORS = {
    "Finalizado":   "#2D8A4E",
    "Em Andamento": "#E8762D",
}

# Data-quality guard: QUANTIDADE values at/above this are treated as data-entry
# errors (the source sheet contains typos up to 10.000.000) and excluded from
# "Total de Peças" / "Média por Chamado". Tune here if the business rule changes.
QUANTIDADE_OUTLIER_CAP = 10000
