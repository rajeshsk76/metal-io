from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
CHARTS_DIR = OUTPUTS_DIR / "charts"

VALUE_CHAIN_STAGES = [
    "1. Deposit Type / Geology",
    "2. Mining / Extraction",
    "3. Concentration / Beneficiation",
    "4. Intermediate Processing / Smelting",
    "5. Refining / Chemical Processing",
    "6. Final Market Product",
]

VALUE_CHAIN_CSV = DATA_DIR / "critical_metals_value_chain_matrix.csv"
MARKET_DATA_CSV = DATA_DIR / "critical_metals_real_data.csv"
CRITICAL_MINERALS_CSV = DATA_DIR / "critical_minerals_2025.csv"
MARKET_STRUCTURED_CSV = DATA_DIR / "critical_metals_market_structured.csv"
COUNTRY_SHARES_CSV = DATA_DIR / "critical_metals_country_shares.csv"