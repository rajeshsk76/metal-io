# metal.io

Critical minerals value chain analysis with a focus on green-industry metals. The project maps supply chains from geology through final market products and supports future Input-Output economic modeling.

**Repository:** https://github.com/rajeshsk76/metal-io

## What it does today

- Maintains the **USGS 2025 list of 60 critical minerals** with canonical `metal_id` slugs
- Defines **6-stage value chains** for 10 key green metals
- Parses market data into **structured numeric fields** (production, reserves, country shares)
- Exports five CSV datasets to `data/`:

| File | Description |
|------|-------------|
| `critical_minerals_2025.csv` | All 60 minerals with green-metal flags |
| `critical_metals_value_chain_matrix.csv` | Stage × metal value chain matrix |
| `critical_metals_real_data.csv` | Human-readable market data (backward compatible) |
| `critical_metals_market_structured.csv` | Parsed production/reserves with numeric columns |
| `critical_metals_country_shares.csv` | Long-format country production shares |

## Project structure

```
metal.io/
├── src/metal_io/
│   ├── data/              # Reference data + metal registry
│   ├── models/            # Typed dataclasses (Metal, MarketRecord, …)
│   ├── parsers/           # Text → numeric/country parsers
│   ├── export/            # DataFrame builders and CSV export
│   ├── loaders.py         # Public data-loading API
│   └── cli.py
├── tests/                 # Data integrity and parser tests
├── data/                  # Generated CSV outputs
├── models/                # Input-Output models (Phase 4)
├── visualizations/        # Charts (Phase 3)
├── notebooks/
├── outputs/
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
# Export all CSVs and print tables
python main.py

# Export only
python main.py --quiet

# Run tests
pytest tests/ -q
```

### Python API

```python
from metal_io import (
    list_critical_minerals,
    load_market_records,
    load_value_chain_matrix,
)

df = load_value_chain_matrix()
records = load_market_records()
for record in records:
    print(record.metal.id, record.production.value_min)
```

## Roadmap

| Phase | Focus | Status |
|-------|-------|--------|
| **1** | Project foundation — modular layout, docs, tooling | Done |
| **2** | Structured data — typed models, metal IDs, parsers | Done |
| **3** | Visualizations — production charts, supply concentration | Next |
| **4** | Input-Output modeling — technology coefficients, scenarios | Planned |
| **5** | Expansion — more metals, external data, CI | Planned |

## License

TBD