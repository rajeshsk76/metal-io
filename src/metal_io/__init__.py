"""metal.io — critical minerals value chain analysis."""

from metal_io.loaders import (
    list_critical_minerals,
    load_market_data,
    load_market_records,
    load_value_chain_matrix,
    load_value_chains,
)
from metal_io.visualize import generate_charts

__version__ = "0.3.0"
__all__ = [
    "list_critical_minerals",
    "load_value_chains",
    "load_value_chain_matrix",
    "load_market_records",
    "load_market_data",
    "generate_charts",
]