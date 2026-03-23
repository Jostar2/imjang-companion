from dataclasses import dataclass, field


@dataclass(slots=True)
class Visit:
    id: str
    property_id: str
    visit_date: str
    status: str = "draft"
    red_flags: list[str] = field(default_factory=list)
    recommendation_notes: str | None = None
    section_scores: dict[str, int] = field(default_factory=dict)
    section_notes: dict[str, str] = field(default_factory=dict)
    attachment_ids: list[str] = field(default_factory=list)
