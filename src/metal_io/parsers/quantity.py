import re

from metal_io.models import ParsedQuantity

_SCALE_WORDS = {
    "thousand": 1_000,
    "million": 1_000_000,
    "billion": 1_000_000_000,
}

_QUALITATIVE = frozenset(
    {"abundant", "china dominant", "significant", "significant; china dominant"}
)


def _to_float(token: str) -> float:
    return float(token.replace(",", "").replace("~", "").strip())


def _apply_scale(value: float, scale_word: str | None) -> float:
    if not scale_word:
        return value
    return value * _SCALE_WORDS[scale_word.lower()]


def parse_quantity(text: str) -> ParsedQuantity:
    raw = text.strip()
    if not raw:
        return ParsedQuantity(None, None, None, raw, notes="empty")

    lowered = raw.lower().rstrip(".")
    if lowered in _QUALITATIVE or "dominant" in lowered and not re.search(r"\d", raw):
        return ParsedQuantity(None, None, None, raw, notes=raw)

    unit_match = re.search(r"\b(tons?|tonnes?|t)\b", raw, re.I)
    unit = "tons" if unit_match else None

    range_match = re.search(
        r"~?\s*([\d,.]+)\s*[–-]\s*([\d,.]+)\s*(thousand|million|billion)?",
        raw,
        re.I,
    )
    if range_match:
        low = _apply_scale(_to_float(range_match.group(1)), range_match.group(3))
        high = _apply_scale(_to_float(range_match.group(2)), range_match.group(3))
        return ParsedQuantity(low, high, unit, raw)

    single_match = re.search(
        r"~?\s*([\d,.]+)\s*(thousand|million|billion)?",
        raw,
        re.I,
    )
    if single_match:
        value = _apply_scale(_to_float(single_match.group(1)), single_match.group(2))
        return ParsedQuantity(value, value, unit, raw)

    embedded_match = re.search(
        r"([\d,.]+)\s*(thousand|million|billion)?\s*(tons?|tonnes?|t)\b",
        raw,
        re.I,
    )
    if embedded_match:
        value = _apply_scale(_to_float(embedded_match.group(1)), embedded_match.group(2))
        return ParsedQuantity(value, value, unit or "tons", raw)

    return ParsedQuantity(None, None, None, raw, notes=raw)