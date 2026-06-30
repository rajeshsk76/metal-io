"""Command-line entry point for metal.io."""

import argparse

from metal_io.data import CRITICAL_MINERALS_2025, GREEN_METAL_IDS
from metal_io.export import export_csvs, validate_green_metal_coverage
from metal_io.loaders import load_market_data, load_value_chain_matrix
from metal_io.dashboard import save_dashboard_html
from metal_io.visualize import generate_charts, save_global_atlas_html


def _run_export(quiet: bool) -> int:
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

    if not quiet:
        print("=" * 100)
        print("CRITICAL METALS VALUE CHAIN MATRIX (Green Industry Focus)")
        print("=" * 100)
        print(df_value_chain.to_string())
        print("\n" + "=" * 100)
        print("\nMARKET DATA (Production, Countries, Companies, Reserves)")
        print("=" * 100)
        print(df_market_data.to_string(index=False))
        print("\n" + "=" * 100)

    return 0


def _run_visualize() -> int:
    validate_green_metal_coverage()
    outputs = generate_charts()

    print("Charts saved:")
    for path in outputs.values():
        print(f"  - {path}")
    return 0


def _run_atlas() -> int:
    validate_green_metal_coverage()
    path = save_global_atlas_html()

    print("Atlas saved:")
    print(f"  - {path}")
    return 0


def _run_dashboard() -> int:
    validate_green_metal_coverage()
    path = save_dashboard_html()

    print("Dashboard saved:")
    print(f"  - {path}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Critical metals data export and visualization toolkit.",
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress table output during export (default command).",
    )
    subparsers = parser.add_subparsers(dest="command")

    export_parser = subparsers.add_parser("export", help="Export datasets to data/ CSV files")
    export_parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress table output; only show summary lines.",
    )

    subparsers.add_parser("visualize", help="Generate charts in outputs/charts/")
    subparsers.add_parser("atlas", help="Generate global critical metals atlas (choropleth HTML)")
    subparsers.add_parser(
        "dashboard",
        help="Build live dashboard (public/index.html) from CSV data",
    )

    args = parser.parse_args(argv)
    command = args.command or "export"

    if command == "visualize":
        return _run_visualize()

    if command == "atlas":
        return _run_atlas()

    if command == "dashboard":
        return _run_dashboard()

    return _run_export(quiet=args.quiet)