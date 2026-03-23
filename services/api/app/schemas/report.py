from pydantic import BaseModel


class ComparisonEntry(BaseModel):
    property_id: str
    address: str
    listing_price_label: str
    total_score: float | None
    visit_id: str | None
    visit_date: str | None
    visit_status: str | None
    strengths: list[str]
    red_flags: list[str]


class ComparisonResponse(BaseModel):
    project_count: int
    project_id: str
    project_name: str
    property_count: int
    entries: list[ComparisonEntry]


class ReportSection(BaseModel):
    title: str
    body: str


class VisitReportResponse(BaseModel):
    project_id: str
    project_name: str
    visit_id: str
    visit_date: str
    property_id: str
    address: str
    total_score: float | None
    sections: list[ReportSection]
