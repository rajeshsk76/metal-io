import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from metal_io.dashboard import build_dashboard_payload, save_dashboard_html


def test_build_dashboard_payload_from_csv_pipeline():
    payload = build_dashboard_payload()
    assert len(payload["metals"]) == 10
    lithium = next(m for m in payload["metals"] if m["id"] == "lithium")
    assert lithium["countries"]
    assert any(c["iso3"] == "AUS" for c in lithium["countries"])


def test_save_dashboard_html(tmp_path):
    path = save_dashboard_html(tmp_path / "index.html")
    html = path.read_text(encoding="utf-8")
    assert "Global Critical Metals Atlas" in html
    assert "plotly" in html.lower()
    data = json.loads(html.split('type="application/json">')[1].split("</script>")[0])
    assert data["metals"][0]["name"]