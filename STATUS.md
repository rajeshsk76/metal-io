# metal.io — Project Status

**Version:** 0.3.0  
**Last updated:** June 2026  
**Repository:** https://github.com/rajeshsk76/metal-io  
**Live dashboard:** https://metal.calvyx.com  

---

## Summary

metal.io is a Python toolkit for critical-minerals value chain analysis, focused on green-industry metals. Phases 1–3 are complete. The project exports structured CSV datasets, generates visualizations, and builds a static live dashboard served at metal.calvyx.com.

**Input-Output economic modeling (Phase 4) has not started.**

---

## Phase progress

| Phase | Scope | Status |
|-------|--------|--------|
| **1** | Modular `src/` layout, CLI, README, `.gitignore`, tests | ✅ Complete |
| **2** | Canonical metal IDs, typed models, parsers, 5 CSV exports | ✅ Complete |
| **3** | Charts (matplotlib + Plotly), global atlas choropleth | ✅ Complete |
| **3b** | Live dashboard (`public/index.html`) for Nginx | ✅ Complete |
| **4** | Input-Output modeling — technology coefficients, scenarios | ⏳ Not started |
| **5** | More metals, external data (USGS), CI/CD | 📋 Planned |

---

## Data coverage

| Dataset | Count | Notes |
|---------|-------|-------|
| USGS critical minerals (2026 list) | 60 | Reference registry with `metal_id` |
| Green-metal value chains | 10 | 6 stages each (geology → final product) |
| Market data (production, reserves, countries) | 10 | Parsed into structured numeric fields |
| Country production shares | ~40 rows | Long-format CSV |

**Green metals:** Lithium, Cobalt, Nickel, Graphite, Copper, Manganese, Silicon, Aluminum, Neodymium, Zinc.

---

## What works today

### CLI

| Command | Output |
|---------|--------|
| `python main.py` | Export 5 CSVs to `data/` |
| `python main.py export --quiet` | Export only, no console tables |
| `python main.py visualize` | Charts in `outputs/charts/` |
| `python main.py atlas` | Standalone atlas HTML (choropleth) |
| `python main.py dashboard` | Live dashboard `public/index.html` |

### Python API

```python
from metal_io import (
    load_value_chain_matrix,
    load_market_records,
    load_market_data,
    generate_charts,
)
```

### Automated tests

**15 tests passing** (`pytest tests/ -q`) — parsers, metal registry, visualizations, atlas, dashboard.

---

## Outputs

### CSV (`data/` — committed to git)

- `critical_minerals_2025.csv`
- `critical_metals_value_chain_matrix.csv`
- `critical_metals_real_data.csv`
- `critical_metals_market_structured.csv`
- `critical_metals_country_shares.csv`

### Charts (`outputs/charts/` — gitignored, regenerate locally)

- Production bar chart (PNG + HTML)
- Supply concentration (PNG)
- Country shares (HTML)
- Value chain heatmap (PNG)
- Global critical metals atlas (HTML)

### Live site (`public/` — committed)

- `index.html` — self-contained dark-theme dashboard; data embedded at build time from CSVs

---

## Architecture

```
src/metal_io/
├── data/          # Static reference data + metal registry
├── models/        # Dataclasses (Metal, MarketRecord, …)
├── parsers/       # Text → numeric / country parsers
├── export/        # CSV builders
├── visualize/     # Charts + global atlas
├── dashboard/     # Live HTML builder (metal.calvyx.com)
├── loaders.py     # Public data API
└── cli.py         # Command-line entry
```

**Entry point:** `main.py` (thin wrapper)

---

## Deployment

Rebuild and deploy the live dashboard after CSV changes:

```bash
cd /opt/metal.io
source venv/bin/activate
python main.py export --quiet
python main.py dashboard
sudo cp public/index.html /var/www/metal.calvyx.com/index.html
```

---

## Known limitations

- **50 of 60 minerals** have no value chain or market data yet
- **Country reserves** are not available per country; reserves map uses production-share geography as a proxy
- **Silicon production** has qualitative (non-numeric) global totals
- **Metal name alignment** is handled via canonical `metal_id`; legacy display names preserved in CSVs
- **`models/`** (IO economic models) and **`notebooks/`** are scaffolded but empty
- **No CI pipeline** — tests run manually
- **Version** remains 0.3.0; dashboard/atlas added within this release cycle

---

## Next recommended step

**Phase 4 — Input-Output modeling**

Scope a first tractable slice (e.g. battery metals: Li + Co + Ni + Graphite → EV cell) with technology coefficients and a simple demand scenario runner in `models/`.

---

## Quick health check

```bash
cd /opt/metal.io && source venv/bin/activate
pytest tests/ -q && python main.py export --quiet && python main.py dashboard
```

Expected: 15 passed, 5 CSVs written, `public/index.html` updated.