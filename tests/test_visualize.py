import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from metal_io.visualize import generate_charts


def test_generate_charts_creates_all_artifacts(tmp_path):
    outputs = generate_charts(tmp_path)

    assert len(outputs) == 6
    for path in outputs.values():
        assert path.exists()
        assert path.stat().st_size > 0