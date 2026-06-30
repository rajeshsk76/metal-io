"""
Build the static live dashboard (public/index.html).

Reads project CSV data via metal_io loaders and bakes JSON into a single
self-contained HTML file for Nginx static hosting.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from metal_io.config import PROJECT_ROOT
from metal_io.loaders import load_market_records
from metal_io.visualize.global_atlas import COUNTRY_TO_ISO3

PUBLIC_DIR = PROJECT_ROOT / "public"
DASHBOARD_HTML = PUBLIC_DIR / "index.html"


def _midpoint(min_val: float | None, max_val: float | None) -> float | None:
    if min_val is None and max_val is None:
        return None
    if min_val is None:
        return max_val
    if max_val is None:
        return min_val
    return (min_val + max_val) / 2


def build_dashboard_payload() -> dict:
    """Serialize market + country data from CSV pipeline for the live dashboard."""
    metals = []

    for record in load_market_records():
        world_tons = _midpoint(record.production.value_min, record.production.value_max)
        countries = []

        for share in record.countries:
            iso3 = COUNTRY_TO_ISO3.get(share.country)
            if not iso3:
                continue
            production_tons = None
            if world_tons is not None and share.share_pct_mid is not None:
                production_tons = world_tons * share.share_pct_mid / 100
            countries.append(
                {
                    "name": share.country,
                    "iso3": iso3,
                    "share_pct_min": share.share_pct_min,
                    "share_pct_max": share.share_pct_max,
                    "share_pct": share.share_pct_mid,
                    "production_tons": production_tons,
                }
            )

        metals.append(
            {
                "id": record.metal.id,
                "name": record.metal.display_name,
                "production_year": record.production_year,
                "production_raw": record.production_raw,
                "reserves_raw": record.reserves_raw,
                "world_production_tons": world_tons,
                "companies": record.companies_raw,
                "countries": countries,
            }
        )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_files": [
            "data/critical_metals_real_data.csv",
            "data/critical_metals_country_shares.csv",
            "data/critical_metals_market_structured.csv",
        ],
        "metals": metals,
    }


def _html_template(payload_json: str) -> str:
    """Return the complete self-contained dashboard HTML."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Global Critical Metals Atlas | metal.io</title>
  <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
  <style>
    :root {{
      --bg: #0b1120;
      --surface: #131c2e;
      --surface-2: #1a2540;
      --border: #243049;
      --text: #e8edf5;
      --muted: #8b9cb3;
      --accent: #3db8cf;
      --accent-dim: #1e6b7a;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      line-height: 1.5;
    }}
    header {{
      border-bottom: 1px solid var(--border);
      background: linear-gradient(180deg, var(--surface) 0%, var(--bg) 100%);
      padding: 1.25rem 2rem;
    }}
    header h1 {{
      font-size: 1.35rem;
      font-weight: 600;
      letter-spacing: -0.02em;
    }}
    header p {{
      color: var(--muted);
      font-size: 0.9rem;
      margin-top: 0.25rem;
    }}
    .layout {{
      display: grid;
      grid-template-columns: 280px 1fr;
      gap: 0;
      min-height: calc(100vh - 88px);
    }}
    aside {{
      border-right: 1px solid var(--border);
      background: var(--surface);
      padding: 1.5rem;
      display: flex;
      flex-direction: column;
      gap: 1.25rem;
    }}
    label {{
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--muted);
      display: block;
      margin-bottom: 0.4rem;
    }}
    select {{
      width: 100%;
      background: var(--surface-2);
      color: var(--text);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 0.65rem 0.75rem;
      font-size: 0.95rem;
      outline: none;
    }}
    select:focus {{ border-color: var(--accent); }}
    .stat {{
      background: var(--surface-2);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 0.85rem 1rem;
    }}
    .stat .value {{
      font-size: 1.05rem;
      font-weight: 600;
      color: var(--accent);
      margin-top: 0.15rem;
    }}
    .stat .caption {{
      font-size: 0.8rem;
      color: var(--muted);
      margin-top: 0.35rem;
    }}
    main {{
      padding: 1rem 1.25rem 1.5rem;
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
    }}
    #map {{
      flex: 1;
      min-height: 520px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      overflow: hidden;
    }}
    footer {{
      border-top: 1px solid var(--border);
      padding: 0.75rem 2rem;
      font-size: 0.78rem;
      color: var(--muted);
      display: flex;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 0.5rem;
    }}
    footer a {{ color: var(--accent); text-decoration: none; }}
    @media (max-width: 900px) {{
      .layout {{ grid-template-columns: 1fr; }}
      aside {{ border-right: none; border-bottom: 1px solid var(--border); }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>Global Critical Metals Atlas</h1>
    <p>Interactive world production map · metal.io · data from project CSVs</p>
  </header>

  <div class="layout">
    <aside>
      <div>
        <label for="metal-select">Critical metal</label>
        <select id="metal-select" aria-label="Select metal"></select>
      </div>
      <div class="stat">
        <label>World production</label>
        <div class="value" id="stat-production">—</div>
        <div class="caption" id="stat-production-year"></div>
      </div>
      <div class="stat">
        <label>World reserves</label>
        <div class="value" id="stat-reserves">—</div>
      </div>
      <div class="stat">
        <label>Top producer</label>
        <div class="value" id="stat-top-country">—</div>
        <div class="caption" id="stat-top-share"></div>
      </div>
      <div class="stat">
        <label>Major producers</label>
        <div class="caption" id="stat-companies" style="margin-top:0.15rem;color:var(--text);font-size:0.82rem;">—</div>
      </div>
    </aside>

    <main>
      <div id="map" role="img" aria-label="World choropleth map of metal production by country"></div>
    </main>
  </div>

  <footer>
    <span id="footer-generated">Generated from metal.io CSV datasets</span>
    <span>
      <a href="https://github.com/rajeshsk76/metal-io" target="_blank" rel="noopener">GitHub</a>
      · metal.calvyx.com
    </span>
  </footer>

  <script id="metal-io-data" type="application/json">{payload_json}</script>
  <script>
    // ── Data (embedded at build time from CSV files) ──────────────────────
    const DATA = JSON.parse(document.getElementById("metal-io-data").textContent);

    const COLORSCALE = [
      [0, "#0f2d3d"],
      [0.25, "#155e75"],
      [0.5, "#22a3b8"],
      [0.75, "#5eead4"],
      [1, "#ccfbf1"],
    ];

    const GEO_LAYOUT = {{
      showframe: false,
      showcoastlines: true,
      coastlinecolor: "#334155",
      showland: true,
      landcolor: "#1a2540",
      showocean: true,
      oceancolor: "#0b1120",
      showcountries: true,
      countrycolor: "#243049",
      bgcolor: "rgba(0,0,0,0)",
      projection: {{ type: "natural earth" }},
    }};

    function formatTons(value) {{
      if (value == null || Number.isNaN(value)) return "Not reported";
      if (value >= 1e9) return (value / 1e9).toFixed(2) + " billion tons";
      if (value >= 1e6) return (value / 1e6).toFixed(2) + " million tons";
      if (value >= 1e3) return (value / 1e3).toFixed(0) + " thousand tons";
      return value.toLocaleString() + " tons";
    }}

    function formatShare(country) {{
      if (country.share_pct == null) return "Share not reported";
      if (country.share_pct_min != null && country.share_pct_max != null &&
          country.share_pct_min !== country.share_pct_max) {{
        return country.share_pct_min + "–" + country.share_pct_max + "% of global";
      }}
      return country.share_pct.toFixed(1) + "% of global";
    }}

    function topProducer(countries) {{
      const ranked = countries
        .filter((c) => c.share_pct != null)
        .sort((a, b) => b.share_pct - a.share_pct);
      return ranked[0] || null;
    }}

    function buildChoropleth(metal) {{
      const withData = metal.countries.filter((c) => c.production_tons != null && c.production_tons > 0);
      const zMax = Math.max(...withData.map((c) => c.production_tons), 1);

      const hover = withData.map((c) =>
        "<b>" + c.name + "</b><br>" +
        "Metal: " + metal.name + "<br>" +
        "Production: " + formatTons(c.production_tons) + "<br>" +
        "Global share: " + formatShare(c) + "<br>" +
        "World total: " + metal.production_raw +
        "<extra></extra>"
      );

      return {{
        type: "choropleth",
        locationmode: "ISO-3",
        locations: withData.map((c) => c.iso3),
        z: withData.map((c) => c.production_tons),
        text: hover,
        hovertemplate: "%{{text}}",
        colorscale: COLORSCALE,
        zmin: 0,
        zmax: zMax,
        colorbar: {{
          title: "Production (tons)",
          titlefont: {{ color: "#8b9cb3", size: 12 }},
          tickfont: {{ color: "#8b9cb3", size: 11 }},
          bgcolor: "rgba(19,28,46,0.9)",
          bordercolor: "#243049",
          borderwidth: 1,
          len: 0.75,
          thickness: 14,
        }},
        marker: {{ line: {{ color: "#243049", width: 0.5 }} }},
      }};
    }}

    function updateSidebar(metal) {{
      document.getElementById("stat-production").textContent = metal.production_raw || "—";
      document.getElementById("stat-production-year").textContent =
        metal.production_year ? "Year: " + metal.production_year : "";
      document.getElementById("stat-reserves").textContent = metal.reserves_raw || "—";
      document.getElementById("stat-companies").textContent = metal.companies || "—";

      const top = topProducer(metal.countries);
      if (top) {{
        document.getElementById("stat-top-country").textContent = top.name;
        document.getElementById("stat-top-share").textContent = formatShare(top);
      }} else {{
        document.getElementById("stat-top-country").textContent = "—";
        document.getElementById("stat-top-share").textContent = "";
      }}
    }}

    function renderMap(metal) {{
      updateSidebar(metal);
      const trace = buildChoropleth(metal);
      const layout = {{
        paper_bgcolor: "#131c2e",
        plot_bgcolor: "#131c2e",
        margin: {{ l: 0, r: 0, t: 10, b: 0 }},
        geo: GEO_LAYOUT,
        font: {{ family: "Inter, system-ui, sans-serif", color: "#e8edf5" }},
      }};
      Plotly.react("map", [trace], layout, {{
        displayModeBar: true,
        displaylogo: false,
        modeBarButtonsToRemove: ["lasso2d", "select2d"],
        scrollZoom: true,
        responsive: true,
      }});
    }}

    // ── Init ───────────────────────────────────────────────────────────────
    const select = document.getElementById("metal-select");
    DATA.metals.forEach((metal, idx) => {{
      const opt = document.createElement("option");
      opt.value = idx;
      opt.textContent = metal.name;
      select.appendChild(opt);
    }});

    document.getElementById("footer-generated").textContent =
      "Built " + new Date(DATA.generated_at).toUTCString() +
      " · Sources: " + DATA.source_files.join(", ");

    select.addEventListener("change", () => {{
      renderMap(DATA.metals[Number(select.value)]);
    }});

    renderMap(DATA.metals[0]);
    window.addEventListener("resize", () => Plotly.Plots.resize("map"));
  </script>
</body>
</html>
"""


def save_dashboard_html(path: Path | None = None) -> Path:
    """Build and write the live dashboard HTML from CSV-backed project data."""
    output = path or DASHBOARD_HTML
    output.parent.mkdir(parents=True, exist_ok=True)

    payload = build_dashboard_payload()
    payload_json = json.dumps(payload, indent=2)
    output.write_text(_html_template(payload_json), encoding="utf-8")
    return output