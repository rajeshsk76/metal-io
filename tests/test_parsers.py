import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from metal_io.parsers import parse_companies, parse_country_shares, parse_quantity


def test_parse_quantity_single_million():
    result = parse_quantity("~3.9 million tons")
    assert result.value_min == 3_900_000
    assert result.value_max == 3_900_000
    assert result.unit == "tons"


def test_parse_quantity_range():
    result = parse_quantity("~1.4 – 1.8 million tons")
    assert result.value_min == 1_400_000
    assert result.value_max == 1_800_000


def test_parse_quantity_qualitative():
    result = parse_quantity("China dominant")
    assert result.is_numeric is False
    assert result.notes == "China dominant"


def test_parse_country_shares_with_ranges():
    shares = parse_country_shares("DRC (~74-76%), Indonesia, Australia")
    assert shares[0].country == "DRC"
    assert shares[0].share_pct_min == 74
    assert shares[0].share_pct_max == 76
    assert shares[1].country == "Indonesia"
    assert shares[1].share_pct_min is None


def test_parse_companies():
    companies = parse_companies("Glencore, Vale, BHP")
    assert companies == ["Glencore", "Vale", "BHP"]