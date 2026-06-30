"""Command-line entry point for metal.io."""

import argparse

from metal_io.data import CRITICAL_MINERALS_2025, GREEN_METAL_IDS
from metal_io.export import export_csvs, validate_green_metal_coverage
from metal_io.loaders import load_market_data, load_value_chain_matrix


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Export critical metals datasets to CSV.",
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress table output; only show summary lines.",
    )
    args = parser.parse_args(argv)

    validate_green_metal_coverage()

    print(f"Loaded {len(CRITICAL_MINERALS_2025)} critical minerals (USGS 2025 list).")
    print(f"Loaded {len(GREEN_METAL_IDS)} green-metal value chains with market data.\n")

    df_value_chain = load_value_chain_matrix()
    df_market_data = load_market_data()
    exports = export_csvs()

    print("Files saved:")
    for path in exports.values():
        print(f"  - {path}")
    print()

    if not args.quiet:
        print("=" * 100)
        print("CRITICAL METALS VALUE CHAIN MATRIX (Green Industry Focus)")
        print("=" * 100)
        print(df_value_chain.to_string())
        print("\n" + "=" * 100)
        print("\nMARKET DATA (Production, Countries, Companies, Reserves)")
        print("=" * 100)
        print(df_market_data.to_string(index=False))
        print("\n" + "=" * 100)

    print("\nDone.")
    return 0