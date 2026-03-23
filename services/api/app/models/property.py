from dataclasses import dataclass


@dataclass(slots=True)
class Property:
    id: str
    project_id: str
    address: str
    listing_price: int | None = None
    property_type: str | None = None
    source: str | None = None
