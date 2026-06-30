from pathlib import Path

from metal_io.config import CHARTS_DIR
from metal_io.visualize.country_shares import save_country_shares_html, save_supply_concentration_png
from metal_io.visualize.production import save_production_bar_html, save_production_bar_png
from metal_io.visualize.value_chain import save_value_chain_heatmap_png


def generate_charts(output_dir: Path | None = None) -> dict[str, Path]:
    charts_dir = output_dir or CHARTS_DIR
    charts_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "production_png": save_production_bar_png(charts_dir / "production_by_metal.png"),
        "production_html": save_production_bar_html(charts_dir / "production_by_metal.html"),
        "concentration_png": save_supply_concentration_png(charts_dir / "supply_concentration.png"),
        "country_shares_html": save_country_shares_html(charts_dir / "country_shares.html"),
        "value_chain_png": save_value_chain_heatmap_png(charts_dir / "value_chain_heatmap.png"),
    }
    return outputs