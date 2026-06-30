from dataclasses import dataclass, field


@dataclass(frozen=True)
class Metal:
    """Canonical identifier for a mineral/metal entry."""

    id: str
    usgs_name: str
    display_name: str
    is_green_metal: bool = False
    has_value_chain: bool = False
    has_market_data: bool = False


@dataclass(frozen=True)
class CriticalMineral:
    metal: Metal


@dataclass
class ParsedQuantity:
    value_min: float | None
    value_max: float | None
    unit: str | None
    raw: str
    notes: str | None = None

    @property
    def is_numeric(self) -> bool:
        return self.value_min is not None or self.value_max is not None


@dataclass(frozen=True)
class CountryShare:
    country: str
    share_pct_min: float | None
    share_pct_max: float | None

    @property
    def share_pct_mid(self) -> float | None:
        if self.share_pct_min is None and self.share_pct_max is None:
            return None
        if self.share_pct_min is None:
            return self.share_pct_max
        if self.share_pct_max is None:
            return self.share_pct_min
        return (self.share_pct_min + self.share_pct_max) / 2


@dataclass
class MarketRecord:
    metal: Metal
    production: ParsedQuantity
    production_year: int | None
    countries: list[CountryShare] = field(default_factory=list)
    companies: list[str] = field(default_factory=list)
    reserves: ParsedQuantity | None = None
    production_raw: str = ""
    countries_raw: str = ""
    companies_raw: str = ""
    reserves_raw: str = ""


@dataclass
class ValueChain:
    metal: Metal
    stages: list[str]