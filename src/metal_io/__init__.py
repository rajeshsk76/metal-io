"""metal.io — critical minerals value chain analysis."""

from metal_io.loaders import (
    list_critical_minerals,
    load_market_data,
    load_market_records,
    load_value_chain_matrix,
    load_value_chains,
)

__version__ = "0.2.0"
__all__ = [
    "list_critical_minerals",
    "load_value_chains",
    "load_value_chain_matrix",
    "load_market_records",
    "load_market_data",
]