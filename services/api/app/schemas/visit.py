from pydantic import BaseModel, Field

from services.api.app.schemas.attachment import AttachmentCreate, AttachmentResponse


class VisitCreate(BaseModel):
    property_id: str = Field(min_length=1)
    visit_date: str = Field(min_length=1, max_length=40)


class ChecklistSectionInput(BaseModel):
    section_name: str = Field(min_length=1, max_length=80)
    score: int = Field(ge=1, le=5)
    note: str = Field(min_length=1, max_length=1000)


class VisitUpdate(BaseModel):
    sections: list[ChecklistSectionInput] = Field(default_factory=list)
    red_flags: list[str] = Field(default_factory=list)
    recommendation_notes: str | None = Field(default=None, max_length=1000)
    attachments: list[AttachmentCreate] = Field(default_factory=list)
    mark_complete: bool = False


class VisitResponse(BaseModel):
    id: str
    property_id: str
    owner_user_id: str | None = None
    visit_date: str
    status: str
    completed_sections: list[str]
    missing_sections: list[str]
    total_score: float | None
    red_flags: list[str]
    recommendation_notes: str | None
    attachments: list[AttachmentResponse]
