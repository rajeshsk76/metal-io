"""
Global Critical Metals Atlas — interactive world choropleth.

Inspired by clean atlas-style dashboards (e.g. atlas.calvyx.com):
minimal chrome, teal sequential palette, light/dark-friendly backgrounds.
"""

from __future__ import annotations

from pathlib import Path

import plotly.graph_objects as go

from metal_io.config import CHARTS_DIR
from metal_io.loaders import load_market_records
from metal_io.models import CountryShare, MarketRecord

# ISO-3166 alpha-3 codes for Plotly choropleth
COUNTRY_TO_ISO3: dict[str, str] = {
    "Argentina": "ARG",
    "Australia": "AUS",
    "Brazil": "BRA",
    "Canada": "CAN",
    "Chile": "CHL",
    "China": "CHN",
    "DRC": "COD",
    "Gabon": "GAB",
    "Guinea": "GIN",
    "India": "IND",
    "Indonesia": "IDN",
    "Mozambique": "MOZ",
    "Myanmar": "MMR",
    "Norway": "NOR",
    "Peru": "PER",
    "Philippines": "PHL",
    "Russia": "RUS",
    "South Africa": "ZAF",
    "United States": "USA",
    "Zimbabwe": "ZWE",
}

# Calvyx-inspired palette: light canvas, deep teal data emphasis
ATLAS_COLORS = {
    "paper_bg": "#F7F9FB",
    "plot_bg": "#F7F9FB",
    "land": "#E8EDF2",
    "land_line": "#CBD5E1",
    "coastline": "#94A3B8",
    "text": "#1E293B",
    "text_muted": "#64748B",
    "accent": "#0E7490",
    "colorscale": [
        [0.0, "#E0F2F7"],
        [0.25, "#99D6E8"],
        [0.5, "#2A9DB8"],
        [0.75, "#1A7A94"],
        [1.0, "#0C4F63"],
    ],
}

METRIC_LABELS = {
    "production": "Production",
    "reserves": "Reserves (estimated)",
}


def _global_total(record: MarketRecord, metric: str) -> float | None:
    """Return global production or reserves in tons (midpoint of min/max)."""
    quantity = record.production if metric == "production" else record.reserves
    if quantity is None or not quantity.is_numeric:
        return None
    if quantity.value_min is not None and quantity.value_max is not None:
        return (quantity.value_min + quantity.value_max) / 2
    return quantity.value_max or quantity.value_min


def _country_value(
    share: CountryShare,
    global_total: float | None,
) -> float | None:
    """Estimate country-level tons from global total × share %."""
    if share.share_pct_mid is None or global_total is None:
        return None
    return global_total * share.share_pct_mid / 100


def _format_quantity(value: float | None) -> str:
    if value is None:
        return "Not reported"
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f} billion tons"
    if value >= 1_000_000:
        return f"{value / 1_000_000:.2f} million tons"
    if value >= 1_000:
        return f"{value / 1_000:,.0f} thousand tons"
    return f"{value:,.0f} tons"


def _format_share(share: CountryShare) -> str:
    if share.share_pct_mid is None:
        return "Not reported"
    if share.share_pct_min != share.share_pct_max:
        return f"{share.share_pct_min:.0f}–{share.share_pct_max:.0f}%"
    return f"{share.share_pct_mid:.1f}%"


def _build_country_rows(record: MarketRecord, metric: str) -> list[dict]:
    """Build choropleth rows for one metal and metric."""
    global_total = _global_total(record, metric)
    rows = []

    for share in record.countries:
        iso3 = COUNTRY_TO_ISO3.get(share.country)
        if iso3 is None:
            continue

        quantity = _country_value(share, global_total)
        rows.append(
            {
                "iso_alpha": iso3,
                "country": share.country,
                "quantity": quantity,
                "quantity_label": _format_quantity(quantity),
                "share_label": _format_share(share),
                "global_total_label": _format_quantity(global_total),
            }
        )

    return rows


def _choropleth_trace(
    record: MarketRecord,
    metric: str,
    *,
    visible: bool,
) -> go.Choropleth:
    """Create one choropleth trace for a metal + metric combination."""
    rows = _build_country_rows(record, metric)
    metric_label = METRIC_LABELS[metric]
    z_values = [row["quantity"] if row["quantity"] is not None else 0 for row in rows]
    numeric_values = [row["quantity"] for row in rows if row["quantity"] is not None]
    max_z = max(numeric_values, default=1)

    hover = [
        (
            f"<b>{row['country']}</b><br>"
            f"Metal: {record.metal.display_name}<br>"
            f"{metric_label}: {row['quantity_label']}<br>"
            f"Global share: {row['share_label']}<br>"
            f"World total: {row['global_total_label']}"
            "<extra></extra>"
        )
        for row in rows
    ]

    return go.Choropleth(
        locations=[row["iso_alpha"] for row in rows],
        z=z_values,
        text=hover,
        hovertemplate="%{text}",
        locationmode="ISO-3",
        colorscale=ATLAS_COLORS["colorscale"],
        zmin=0,
        zmax=max_z,
        colorbar=dict(
            title=dict(text=metric_label, side="right", font=dict(color=ATLAS_COLORS["text"])),
            tickfont=dict(color=ATLAS_COLORS["text_muted"]),
            len=0.65,
            thickness=14,
            outlinecolor=ATLAS_COLORS["land_line"],
            bgcolor="rgba(255,255,255,0.8)",
        ),
        marker=dict(line=dict(color=ATLAS_COLORS["land_line"], width=0.5)),
        visible=visible,
        name=f"{record.metal.display_name} · {metric_label}",
    )


def _title_html(metal_name: str, metric_label: str) -> str:
    return (
        f"<b>Global Critical Metals Atlas</b><br>"
        f"<span style='font-size:14px;color:{ATLAS_COLORS['text_muted']}'>"
        f"{metal_name} · {metric_label} by country"
        "</span>"
    )


def build_global_atlas_figure() -> go.Figure:
    """Build the interactive atlas with metal and metric selectors."""
    records = load_market_records()
    traces: list[go.Choropleth] = []

    for metal_idx, record in enumerate(records):
        for metric_idx, metric in enumerate(("production", "reserves")):
            traces.append(
                _choropleth_trace(
                    record,
                    metric,
                    visible=(metal_idx == 0 and metric_idx == 0),
                )
            )

    fig = go.Figure(data=traces)

    def _visibility(metal_idx: int, metric_idx: int) -> list[bool]:
        visibility = [False] * len(traces)
        visibility[metal_idx * 2 + metric_idx] = True
        return visibility

    # Full selector: metal × metric (20 options)
    combined_buttons = []
    for metal_idx, record in enumerate(records):
        for metric_idx, metric in enumerate(("production", "reserves")):
            combined_buttons.append(
                dict(
                    label=f"{record.metal.display_name} — {METRIC_LABELS[metric]}",
                    method="update",
                    args=[
                        {"visible": _visibility(metal_idx, metric_idx)},
                        {
                            "title": dict(
                                text=_title_html(record.metal.display_name, METRIC_LABELS[metric]),
                                x=0.5,
                            )
                        },
                    ],
                )
            )

    # Quick metal picker (production only)
    metal_buttons = []
    for metal_idx, record in enumerate(records):
        metal_buttons.append(
            dict(
                label=record.metal.display_name,
                method="update",
                args=[
                    {"visible": _visibility(metal_idx, 0)},
                    {"title": dict(text=_title_html(record.metal.display_name, "Production"), x=0.5)},
                ],
            )
        )

    first = records[0]
    fig.update_layout(
        title=dict(
            text=_title_html(first.metal.display_name, "Production"),
            x=0.5,
            xanchor="center",
            font=dict(size=20, color=ATLAS_COLORS["text"]),
        ),
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor=ATLAS_COLORS["coastline"],
            showland=True,
            landcolor=ATLAS_COLORS["land"],
            showocean=True,
            oceancolor=ATLAS_COLORS["paper_bg"],
            showcountries=True,
            countrycolor=ATLAS_COLORS["land_line"],
            bgcolor=ATLAS_COLORS["plot_bg"],
            projection=dict(type="natural earth"),
        ),
        paper_bgcolor=ATLAS_COLORS["paper_bg"],
        plot_bgcolor=ATLAS_COLORS["plot_bg"],
        font=dict(family="Inter, system-ui, -apple-system, sans-serif", color=ATLAS_COLORS["text"]),
        margin=dict(l=0, r=0, t=90, b=40),
        height=720,
        updatemenus=[
            dict(
                type="dropdown",
                direction="down",
                active=0,
                x=0.01,
                xanchor="left",
                y=1.14,
                yanchor="top",
                bgcolor="rgba(255,255,255,0.95)",
                bordercolor=ATLAS_COLORS["land_line"],
                borderwidth=1,
                font=dict(size=13, color=ATLAS_COLORS["text"]),
                buttons=combined_buttons,
            ),
            dict(
                type="dropdown",
                direction="down",
                active=0,
                x=0.42,
                xanchor="left",
                y=1.14,
                yanchor="top",
                bgcolor="rgba(255,255,255,0.95)",
                bordercolor=ATLAS_COLORS["land_line"],
                borderwidth=1,
                font=dict(size=13, color=ATLAS_COLORS["text"]),
                buttons=metal_buttons,
            ),
        ],
        annotations=[
            dict(
                text=(
                    "Hover for country name, quantity, and global share. "
                    "Reserves estimated from global totals × production-share geography."
                ),
                xref="paper",
                yref="paper",
                x=0.5,
                y=-0.04,
                showarrow=False,
                font=dict(size=11, color=ATLAS_COLORS["text_muted"]),
                align="center",
            ),
        ],
    )

    return fig


def save_global_atlas_html(path: Path | None = None) -> Path:
    """
    Generate and save the Global Critical Metals Atlas as standalone HTML.

    Args:
        path: Output file path. Defaults to outputs/charts/global_critical_metals_atlas.html.

    Returns:
        Path to the saved HTML file.
    """
    output = path or (CHARTS_DIR / "global_critical_metals_atlas.html")
    output.parent.mkdir(parents=True, exist_ok=True)

    fig = build_global_atlas_figure()
    fig.write_html(
        output,
        include_plotlyjs="cdn",
        full_html=True,
        config={
            "displayModeBar": True,
            "displaylogo": False,
            "modeBarButtonsToRemove": ["lasso2d", "select2d"],
            "scrollZoom": True,
        },
    )
    return output