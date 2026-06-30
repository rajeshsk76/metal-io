import re

from metal_io.models import CountryShare

_SHARE_PATTERN = re.compile(
    r"([^,]+?)\s*\(\s*~?\s*([\d.]+)(?:\s*-\s*([\d.]+))?\s*%\s*\)",
    re.I,
)


def parse_country_shares(text: str) -> list[CountryShare]:
    shares: list[CountryShare] = []
    matched_spans: list[tuple[int, int]] = []

    for match in _SHARE_PATTERN.finditer(text):
        country = match.group(1).strip()
        low = float(match.group(2))
        high = float(match.group(3)) if match.group(3) else low
        shares.append(CountryShare(country=country, share_pct_min=low, share_pct_max=high))
        matched_spans.append(match.span())

    remainder = text
    for start, end in reversed(matched_spans):
        remainder = remainder[:start] + remainder[end:]

    for part in remainder.split(","):
        country = part.strip()
        if country:
            shares.append(CountryShare(country=country, share_pct_min=None, share_pct_max=None))

    return shares


def parse_companies(text: str) -> list[str]:
    return [company.strip() for company in text.split(",") if company.strip()]