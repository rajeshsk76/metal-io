from pathlib import Path

import pandas as pd

from metal_io.config import (
    COUNTRY_SHARES_CSV,
    CRITICAL_MINERALS_CSV,
    DATA_DIR,
    MARKET_DATA_CSV,
    MARKET_STRUCTURED_CSV,
    VALUE_CHAIN_CSV,
    VALUE_CHAIN_STAGES,
)
from metal_io.data import GREEN_METAL_IDS, get_metal
from metal_io.loaders import list_critical_minerals, load_market_records, load_value_chains


def build_value_chain_matrix(stages: list[str] | None = None) -> pd.DataFrame:
    stage_list = stages or VALUE_CHAIN_STAGES
    chains = load_value_chains()

    data: dict[str, list[str]] = {}
    for chain in chains:
        stages_for_metal = chain.stages
        if len(stages_for_metal) != len(stage_list):
            stages_for_metal = stages_for_metal[: len(stage_list)] + [""] * (
                len(stage_list) - len(stages_for_metal)
            )
        data[chain.metal.display_name] = stages_for_metal

    df = pd.DataFrame(data, index=stage_list)
    df.index.name = "Value Chain Stage"
    return df


def build_market_data_frame() -> pd.DataFrame:
    rows = []
    for record in load_market_records():
        rows.append(
            {
                "metal_id": record.metal.id,
                "Metal": record.metal.display_name,
                "World Production (latest)": record.production_raw,
                "Top Producing Countries": record.countries_raw,
                "Major Companies / Mines": record.companies_raw,
                "World Reserves": record.reserves_raw,
            }
        )
    return pd.DataFrame(rows)


def build_critical_minerals_frame() -> pd.DataFrame:
    rows = []
    for entry in list_critical_minerals():
        metal = entry.metal
        rows.append(
            {
                "metal_id": metal.id,
                "usgs_name": metal.usgs_name,
                "display_name": metal.display_name,
                "is_green_metal": metal.is_green_metal,
                "has_value_chain": metal.has_value_chain,
                "has_market_data": metal.has_market_data,
            }
        )
    return pd.DataFrame(rows)


def build_market_structured_frame() -> pd.DataFrame:
    rows = []
    for record in load_market_records():
        rows.append(
            {
                "metal_id": record.metal.id,
                "display_name": record.metal.display_name,
                "production_year": record.production_year,
                "production_tons_min": record.production.value_min,
                "production_tons_max": record.production.value_max,
                "production_unit": record.production.unit,
                "production_notes": record.production.notes,
                "production_raw": record.production_raw,
                "reserves_tons_min": record.reserves.value_min if record.reserves else None,
                "reserves_tons_max": record.reserves.value_max if record.reserves else None,
                "reserves_unit": record.reserves.unit if record.reserves else None,
                "reserves_notes": record.reserves.notes if record.reserves else None,
                "reserves_raw": record.reserves_raw,
                "company_count": len(record.companies),
                "companies": "; ".join(record.companies),
            }
        )
    return pd.DataFrame(rows)


def build_country_shares_frame() -> pd.DataFrame:
    rows = []
    for record in load_market_records():
        for share in record.countries:
            rows.append(
                {
                    "metal_id": record.metal.id,
                    "display_name": record.metal.display_name,
                    "country": share.country,
                    "share_pct_min": share.share_pct_min,
                    "share_pct_max": share.share_pct_max,
                    "share_pct_mid": share.share_pct_mid,
                }
            )
    return pd.DataFrame(rows)


def export_csvs(output_dir: Path | None = None) -> dict[str, Path]:
    out = output_dir or DATA_DIR
    out.mkdir(parents=True, exist_ok=True)

    exports = {
        "value_chain": out / VALUE_CHAIN_CSV.name,
        "market_data": out / MARKET_DATA_CSV.name,
        "critical_minerals": out / CRITICAL_MINERALS_CSV.name,
        "market_structured": out / MARKET_STRUCTURED_CSV.name,
        "country_shares": out / COUNTRY_SHARES_CSV.name,
    }

    build_value_chain_matrix().to_csv(exports["value_chain"], encoding="utf-8-sig")
    build_market_data_frame().to_csv(exports["market_data"], index=False, encoding="utf-8-sig")
    build_critical_minerals_frame().to_csv(exports["critical_minerals"], index=False, encoding="utf-8-sig")
    build_market_structured_frame().to_csv(exports["market_structured"], index=False, encoding="utf-8-sig")
    build_country_shares_frame().to_csv(exports["country_shares"], index=False, encoding="utf-8-sig")

    return exports


def validate_green_metal_coverage() -> None:
    """Ensure every green metal has matching value chain and market data."""
    for metal_id in GREEN_METAL_IDS:
        metal = get_metal(metal_id)
        if not metal.has_value_chain or not metal.has_market_data:
            raise ValueError(f"Incomplete green metal registry entry: {metal_id}")