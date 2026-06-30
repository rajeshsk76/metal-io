"""Public data-loading API for metal.io."""

import pandas as pd

from metal_io.data import GREEN_METAL_IDS, MARKET_DATA, METALS, VALUE_CHAINS, get_metal
from metal_io.models import CriticalMineral, MarketRecord, ValueChain
from metal_io.parsers import parse_companies, parse_country_shares, parse_quantity


def _production_field(fields: dict[str, str]) -> tuple[str, int | None]:
    for year in (2025, 2024):
        key = f"World Production ({year})"
        if key in fields:
            return fields[key], year
    return "N/A", None


def list_critical_minerals() -> list[CriticalMineral]:
    return [CriticalMineral(metal=metal) for metal in sorted(METALS.values(), key=lambda m: m.usgs_name)]


def load_value_chains() -> list[ValueChain]:
    chains: list[ValueChain] = []
    for metal_id in GREEN_METAL_IDS:
        metal = get_metal(metal_id)
        chains.append(ValueChain(metal=metal, stages=VALUE_CHAINS[metal_id]))
    return chains


def load_market_records() -> list[MarketRecord]:
    records: list[MarketRecord] = []
    for metal_id in GREEN_METAL_IDS:
        metal = get_metal(metal_id)
        fields = MARKET_DATA[metal_id]
        production_raw, production_year = _production_field(fields)
        countries_raw = fields["Top Producing Countries"]
        companies_raw = fields["Major Companies / Mines"]
        reserves_raw = fields["World Reserves"]

        records.append(
            MarketRecord(
                metal=metal,
                production=parse_quantity(production_raw),
                production_year=production_year,
                countries=parse_country_shares(countries_raw),
                companies=parse_companies(companies_raw),
                reserves=parse_quantity(reserves_raw),
                production_raw=production_raw,
                countries_raw=countries_raw,
                companies_raw=companies_raw,
                reserves_raw=reserves_raw,
            )
        )
    return records


def load_value_chain_matrix() -> pd.DataFrame:
    from metal_io.export.csv_export import build_value_chain_matrix

    return build_value_chain_matrix()


def load_market_data() -> pd.DataFrame:
    from metal_io.export.csv_export import build_market_data_frame

    return build_market_data_frame()