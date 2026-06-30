# metal.io

Critical minerals value chain analysis with a focus on green-industry metals. The project maps supply chains from geology through final market products and supports future Input-Output economic modeling.

**Repository:** https://github.com/rajeshsk76/metal-io

## What it does today

- Maintains the **USGS 2025 list of 60 critical minerals** with canonical `metal_id` slugs
- Defines **6-stage value chains** for 10 key green metals
- Parses market data into **structured numeric fields** (production, reserves, country shares)
- Exports five CSV datasets to `data/`
- Generates interactive and static charts in `outputs/charts/`

| Output | Description |
|--------|-------------|
| `data/critical_minerals_2025.csv` | All 60 minerals with green-metal flags |
| `data/critical_metals_market_structured.csv` | Parsed production/reserves |
| `data/critical_metals_country_shares.csv` | Country production shares |
| `outputs/charts/production_by_metal.png` | Production bar chart (static) |
| `outputs/charts/production_by_metal.html` | Production bar chart (interactive) |
| `outputs/charts/supply_concentration.png` | Top-country share per metal |
| `outputs/charts/country_shares.html` | Country shares by metal (interactive) |
| `outputs/charts/value_chain_heatmap.png` | Value chain detail heatmap |

## Project structure

```
metal.io/
├── src/metal_io/
│   ├── data/              # Reference data + metal registry
│   ├── models/            # Typed dataclasses
│   ├── parsers/           # Text → numeric/country parsers
│   ├── export/            # CSV builders
│   ├── visualize/         # Chart generation (Phase 3)
│   ├── loaders.py         # Public data-loading API
│   └── cli.py
├── tests/
├── data/                  # Generated CSV outputs
├── models/                # IO models (Phase 4)
├── outputs/charts/        # Generated charts (gitignored)
└── main.py
```

## Setup

```bash
cd /opt/metal.io
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
# Export all CSVs (default command)
python main.py
python main.py export --quiet

# Generate charts
python main.py visualize

# Run tests
pytest tests/ -q
```

### Python API

```python
from metal_io import generate_charts, load_market_records

records = load_market_records()
charts = generate_charts()  # writes to outputs/charts/
```

## Roadmap

| Phase | Focus | Status |
|-------|-------|--------|
| **1** | Project foundation | Done |
| **2** | Structured data | Done |
| **3** | Visualizations | Done |
| **4** | Input-Output modeling | Next |
| **5** | Expansion — more metals, external data, CI | Planned |

## License

TBD