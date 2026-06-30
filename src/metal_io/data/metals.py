import re

from metal_io.models import Metal

from .critical_minerals import CRITICAL_MINERALS_2025

_GREEN_METAL_DEFINITIONS: list[dict] = [
    {
        "id": "lithium",
        "usgs_name": "Lithium",
        "display_name": "Lithium",
        "has_value_chain": True,
        "has_market_data": True,
    },
    {
        "id": "cobalt",
        "usgs_name": "Cobalt",
        "display_name": "Cobalt",
        "has_value_chain": True,
        "has_market_data": True,
    },
    {
        "id": "nickel",
        "usgs_name": "Nickel",
        "display_name": "Nickel",
        "has_value_chain": True,
        "has_market_data": True,
    },
    {
        "id": "graphite",
        "usgs_name": "Graphite",
        "display_name": "Graphite (Natural)",
        "has_value_chain": True,
        "has_market_data": True,
    },
    {
        "id": "copper",
        "usgs_name": "Copper",
        "display_name": "Copper",
        "has_value_chain": True,
        "has_market_data": True,
    },
    {
        "id": "manganese",
        "usgs_name": "Manganese",
        "display_name": "Manganese",
        "has_value_chain": True,
        "has_market_data": True,
    },
    {
        "id": "silicon",
        "usgs_name": "Silicon",
        "display_name": "Silicon (Metallurgical/Solar)",
        "has_value_chain": True,
        "has_market_data": True,
    },
    {
        "id": "aluminum",
        "usgs_name": "Aluminum",
        "display_name": "Aluminum",
        "has_value_chain": True,
        "has_market_data": True,
    },
    {
        "id": "neodymium",
        "usgs_name": "Neodymium",
        "display_name": "Neodymium (Rare Earth)",
        "has_value_chain": True,
        "has_market_data": True,
    },
    {
        "id": "zinc",
        "usgs_name": "Zinc",
        "display_name": "Zinc",
        "has_value_chain": True,
        "has_market_data": True,
    },
]


def _slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    return slug or "unknown"


def _build_registry() -> dict[str, Metal]:
    registry: dict[str, Metal] = {}

    for item in _GREEN_METAL_DEFINITIONS:
        metal = Metal(is_green_metal=True, **item)
        registry[metal.id] = metal

    green_usgs_names = {metal.usgs_name for metal in registry.values()}
    for usgs_name in CRITICAL_MINERALS_2025:
        if usgs_name in green_usgs_names:
            continue
        metal_id = _slugify(usgs_name)
        registry[metal_id] = Metal(
            id=metal_id,
            usgs_name=usgs_name,
            display_name=usgs_name,
        )

    return registry


METALS: dict[str, Metal] = _build_registry()
GREEN_METAL_IDS: list[str] = [
    item["id"] for item in _GREEN_METAL_DEFINITIONS
]


def get_metal(metal_id: str) -> Metal:
    if metal_id not in METALS:
        raise KeyError(f"Unknown metal id: {metal_id}")
    return METALS[metal_id]


def list_metals(*, green_only: bool = False) -> list[Metal]:
    metals = [METALS[metal_id] for metal_id in GREEN_METAL_IDS] if green_only else list(METALS.values())
    return sorted(metals, key=lambda metal: metal.usgs_name)