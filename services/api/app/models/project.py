from dataclasses import dataclass


@dataclass(slots=True)
class Project:
    id: str
    name: str
    region: str | None = None
    budget: str | None = None
    notes: str | None = None
