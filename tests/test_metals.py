import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from metal_io.data import CRITICAL_MINERALS_2025, GREEN_METAL_IDS, METALS
from metal_io.export import validate_green_metal_coverage
from metal_io.loaders import list_critical_minerals, load_market_records


def test_registry_covers_all_critical_minerals():
    assert len(METALS) == len(CRITICAL_MINERALS_2025)


def test_green_metals_have_aligned_ids():
    for metal_id in GREEN_METAL_IDS:
        metal = METALS[metal_id]
        assert metal.is_green_metal
        assert metal.has_value_chain
        assert metal.has_market_data


def test_market_records_use_canonical_display_names():
    records = load_market_records()
    display_names = {record.metal.display_name for record in records}
    assert "Silicon (Metallurgical/Solar)" in display_names
    assert "Silicon (Metal)" not in display_names
    assert "Neodymium (Rare Earth)" in display_names


def test_critical_minerals_reference_has_flags():
    minerals = list_critical_minerals()
    green_count = sum(1 for entry in minerals if entry.metal.is_green_metal)
    assert green_count == len(GREEN_METAL_IDS)


def test_validate_green_metal_coverage_passes():
    validate_green_metal_coverage()