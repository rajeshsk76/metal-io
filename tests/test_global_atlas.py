import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from metal_io.visualize.global_atlas import build_global_atlas_figure, save_global_atlas_html


def test_build_global_atlas_figure():
    fig = build_global_atlas_figure()
    assert len(fig.data) == 20  # 10 metals × 2 metrics
    assert fig.layout.geo.projection.type == "natural earth"


def test_save_global_atlas_html(tmp_path):
    path = save_global_atlas_html(tmp_path / "global_critical_metals_atlas.html")
    assert path.exists()
    content = path.read_text(encoding="utf-8")
    assert "Global Critical Metals Atlas" in content
    assert "plotly" in content.lower()