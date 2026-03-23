from pydantic import BaseModel


class ComparisonEntry(BaseModel):
    property_id: str
    address: str
    listing_price_label: str
    total_score: float | None
    strengths: list[str]
    red_flags: list[str]


class ComparisonResponse(BaseModel):
    project_count: int
    entries: list[ComparisonEntry]


class ReportSection(BaseModel):
    title: str
    body: str


class VisitReportResponse(BaseModel):
    property_id: str
    address: str
    total_score: float | None
    sections: list[ReportSection]
