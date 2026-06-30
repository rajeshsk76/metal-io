from pathlib import Path

import matplotlib.pyplot as plt
import plotly.express as px

from metal_io.export.csv_export import build_country_shares_frame
from metal_io.visualize._style import ACCENT_COLOR, FONT_FAMILY, PLOTLY_TEMPLATE


def _shares_with_data():
    df = build_country_shares_frame()
    return df[df["share_pct_mid"].notna()].copy()


def save_supply_concentration_png(path: Path) -> Path:
    """Top-country share (%) per metal — proxy for supply concentration."""
    df = _shares_with_data()
    top = (
        df.sort_values("share_pct_mid", ascending=False)
        .groupby("display_name", as_index=False)
        .first()
        .sort_values("share_pct_mid", ascending=True)
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(top["display_name"], top["share_pct_mid"], color=ACCENT_COLOR)
    ax.set_xlabel("Largest producer share (%)")
    ax.set_title("Green Metals — Supply Concentration (Top Country)")
    ax.set_xlim(0, 100)
    ax.grid(axis="x", alpha=0.3)

    for idx, row in enumerate(top.itertuples()):
        ax.text(row.share_pct_mid + 1, idx, row.country, va="center", fontsize=8)

    ax.bar_label(bars, fmt="%.0f%%", padding=2, fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def save_country_shares_html(path: Path) -> Path:
    df = _shares_with_data()
    path.parent.mkdir(parents=True, exist_ok=True)

    fig = px.bar(
        df.sort_values(["display_name", "share_pct_mid"], ascending=[True, False]),
        x="share_pct_mid",
        y="country",
        color="display_name",
        orientation="h",
        barmode="group",
        facet_col="display_name",
        facet_col_wrap=2,
        labels={"share_pct_mid": "Share (%)", "country": "Country", "display_name": "Metal"},
        title="Green Metals — Production Share by Country",
        template=PLOTLY_TEMPLATE,
        height=900,
    )
    fig.update_layout(showlegend=False)
    fig.write_html(path, include_plotlyjs="cdn")
    return path