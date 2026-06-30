# metal.io

Critical minerals value chain analysis for green-industry metals — from geology to final market products, with structured market data, visualizations, and a path toward Input-Output economic modeling.

**Repository:** https://github.com/rajeshsk76/metal-io  
**Version:** 0.3.0

---

## Overview

metal.io tracks the global supply chain for metals critical to the energy transition. The project combines:

- The **USGS 2025 list of 60 critical minerals**
- **6-stage value chains** for 10 key green metals
- **Market intelligence** — production, reserves, country shares, major producers
- **Structured data exports** (CSV) and **charts** (PNG + interactive HTML)

### Green metals covered (10)

| Metal | `metal_id` |
|-------|------------|
| Lithium | `lithium` |
| Cobalt | `cobalt` |
| Nickel | `nickel` |
| Graphite (Natural) | `graphite` |
| Copper | `copper` |
| Manganese | `manganese` |
| Silicon (Metallurgical/Solar) | `silicon` |
| Aluminum | `aluminum` |
| Neodymium (Rare Earth) | `neodymium` |
| Zinc | `zinc` |

### Value chain stages

1. Deposit Type / Geology  
2. Mining / Extraction  
3. Concentration / Beneficiation  
4. Intermediate Processing / Smelting  
5. Refining / Chemical Processing  
6. Final Market Product  

---

## Quick start

```bash
cd /opt/metal.io
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python main.py              # export CSVs to data/
python main.py visualize    # generate charts in outputs/charts/
pytest tests/ -q            # run tests (11 passing)
```

---

## Usage

### CLI commands

| Command | Description |
|---------|-------------|
| `python main.py` | Export all CSV datasets (default) |
| `python main.py export --quiet` | Export only, no table output |
| `python main.py visualize` | Generate all charts |

### Python API

```python
from metal_io import (
    generate_charts,
    load_market_data,
    load_market_records,
    load_value_chain_matrix,
)

# DataFrames
df_chains = load_value_chain_matrix()
df_market = load_market_data()

# Typed records with parsed numeric fields
for record in load_market_records():
    print(record.metal.id, record.production.value_min)

# Charts → outputs/charts/
generate_charts()
```

---

## Outputs

### CSV datasets (`data/`)

| File | Description |
|------|-------------|
| `critical_minerals_2025.csv` | All 60 USGS minerals with `metal_id` and coverage flags |
| `critical_metals_value_chain_matrix.csv` | Stage × metal value chain matrix |
| `critical_metals_real_data.csv` | Human-readable market data |
| `critical_metals_market_structured.csv` | Parsed production/reserves (numeric columns) |
| `critical_metals_country_shares.csv` | Country production shares (long format) |

Regenerate with `python main.py`.

### Charts (`outputs/charts/` — gitignored)

| File | Type | Description |
|------|------|-------------|
| `production_by_metal.png` | Static | World production bar chart |
| `production_by_metal.html` | Interactive | Production bar chart (Plotly) |
| `supply_concentration.png` | Static | Top-country share per metal |
| `country_shares.html` | Interactive | Country shares faceted by metal |
| `value_chain_heatmap.png` | Static | Value chain detail heatmap |

Regenerate with `python main.py visualize`.

---

## Project structure

```
metal.io/
├── main.py                     # Entry point
├── requirements.txt
├── src/metal_io/
│   ├── cli.py                  # CLI (export, visualize)
│   ├── config.py               # Paths and constants
│   ├── loaders.py              # Public data-loading API
│   ├── data/
│   │   ├── critical_minerals.py
│   │   ├── value_chains.py
│   │   ├── market_data.py
│   │   └── metals.py           # Canonical metal registry
│   ├── models/                 # Dataclasses (Metal, MarketRecord, …)
│   ├── parsers/                # Text → numeric/country parsers
│   ├── export/                 # CSV builders
│   └── visualize/              # Chart generation
├── tests/                      # pytest suite
├── data/                       # Generated CSVs (committed)
├── models/                     # IO economic models (Phase 4)
├── notebooks/                  # Exploratory analysis
├── visualizations/             # Reserved for future assets
└── outputs/                    # Generated charts (gitignored)
```

---

## Development

### Dependencies

- **Core:** pandas, numpy  
- **Charts:** matplotlib, plotly  
- **Tests:** pytest  

### Run tests

```bash
pytest tests/ -q
```

### Git

```bash
git remote -v   # origin → git@github.com:rajeshsk76/metal-io.git
```

---

## Roadmap

| Phase | Focus | Status |
|-------|-------|--------|
| **1** | Project foundation — modular `src/` layout, docs, tooling | ✅ Done |
| **2** | Structured data — metal IDs, typed models, parsers, 5 CSVs | ✅ Done |
| **3** | Visualizations — production, concentration, value chain charts | ✅ Done |
| **4** | Input-Output modeling — technology coefficients, demand scenarios | 🔜 Next |
| **5** | Expansion — more metals, USGS data integration, CI | Planned |

---

## License

TBD