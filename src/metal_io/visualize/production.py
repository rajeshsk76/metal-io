from pathlib import Path

import matplotlib.pyplot as plt
import plotly.graph_objects as go

from metal_io.loaders import load_market_records
from metal_io.visualize._style import ACCENT_COLOR, FONT_FAMILY, METAL_COLOR, PLOTLY_TEMPLATE


def _production_tons(record) -> float | None:
    production = record.production
    if not production.is_numeric:
        return None
    if production.value_max is not None:
        return production.value_max
    return production.value_min


def build_production_dataframe():
    import pandas as pd

    rows = []
    for record in load_market_records():
        tons = _production_tons(record)
        if tons is None:
            continue
        rows.append(
            {
                "metal_id": record.metal.id,
                "display_name": record.metal.display_name,
                "production_tons": tons,
                "production_year": record.production_year,
            }
        )
    df = pd.DataFrame(rows)
    return df.sort_values("production_tons", ascending=True)


def save_production_bar_png(path: Path) -> Path:
    df = build_production_dataframe()
    path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(df["display_name"], df["production_tons"] / 1_000_000, color=METAL_COLOR)
    ax.set_xlabel("World production (million tons)")
    ax.set_title("Green Metals — World Production")
    ax.grid(axis="x", alpha=0.3, color="#E8EEF2")
    ax.bar_label(bars, fmt="%.1f", padding=4, fontsize=8)

    for label in ax.get_yticklabels():
        label.set_fontfamily("DejaVu Sans")

    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def save_production_bar_html(path: Path) -> Path:
    df = build_production_dataframe().sort_values("production_tons", ascending=False)
    path.parent.mkdir(parents=True, exist_ok=True)

    fig = go.Figure(
        go.Bar(
            x=df["display_name"],
            y=df["production_tons"],
            marker_color=METAL_COLOR,
            text=[f"{v / 1e6:.1f}M" if v >= 1e6 else f"{v / 1e3:.0f}K" for v in df["production_tons"]],
            textposition="outside",
            hovertemplate="%{x}<br>Production: %{y:,.0f} tons<extra></extra>",
        )
    )
    fig.update_layout(
        title="Green Metals — World Production",
        xaxis_title="Metal",
        yaxis_title="Production (tons)",
        template=PLOTLY_TEMPLATE,
        height=520,
    )
    fig.write_html(path, include_plotlyjs="cdn")
    return path