from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from services.api.app.core.auth import get_current_user, require_global_scope
from services.api.app.core.db import ProjectRecord, PropertyRecord, UserRecord, VisitRecord, get_session
from services.api.app.schemas.report import ComparisonEntry, ComparisonResponse, ReportSection, VisitReportResponse

router = APIRouter(prefix="/reports", tags=["reports"])


def format_price(value: int | None) -> str:
    if value is None:
        return "TBD"
    return f"{value:,} KRW"


@router.get("/comparison", response_model=ComparisonResponse)
def comparison(
    owner_user_id: str | None = None,
    session: Session = Depends(get_session),
    current_user: UserRecord = Depends(get_current_user),
) -> ComparisonResponse:
    target_owner_user_id = current_user.id
    if owner_user_id is not None:
        require_global_scope("all", current_user)
        target_owner_user_id = owner_user_id

    properties = session.scalars(
        select(PropertyRecord)
        .join(ProjectRecord, PropertyRecord.project_id == ProjectRecord.id)
        .where(ProjectRecord.owner_user_id == target_owner_user_id)
        .order_by(PropertyRecord.id)
    ).all()

    entries: list[ComparisonEntry] = []
    for property_item in properties:
        latest_visit = session.scalars(
            select(VisitRecord)
            .where(VisitRecord.property_id == property_item.id)
            .order_by(VisitRecord.id.desc())
        ).first()
        section_scores = latest_visit.section_scores if latest_visit and latest_visit.section_scores else {}
        score_values = list(section_scores.values())
        total_score = round(sum(score_values) / len(score_values), 2) if score_values else None
        strengths = (
            [f"{section} section completed" for section in sorted(section_scores.keys())[:3]]
            if section_scores
            else ["No completed visit yet"]
        )
        red_flags = latest_visit.red_flags if latest_visit and latest_visit.red_flags else ["No red flags recorded"]
        entries.append(
            ComparisonEntry(
                property_id=property_item.id,
                address=property_item.address,
                listing_price_label=format_price(property_item.listing_price),
                total_score=total_score,
                strengths=strengths,
                red_flags=red_flags,
            )
        )

    return ComparisonResponse(project_count=len(entries), entries=entries)


@router.get("/latest", response_model=VisitReportResponse)
def latest_report(
    owner_user_id: str | None = None,
    session: Session = Depends(get_session),
    current_user: UserRecord = Depends(get_current_user),
) -> VisitReportResponse:
    target_owner_user_id = current_user.id
    if owner_user_id is not None:
        require_global_scope("all", current_user)
        target_owner_user_id = owner_user_id

    latest_visit = session.scalars(
        select(VisitRecord)
        .join(PropertyRecord, VisitRecord.property_id == PropertyRecord.id)
        .join(ProjectRecord, PropertyRecord.project_id == ProjectRecord.id)
        .where(ProjectRecord.owner_user_id == target_owner_user_id, VisitRecord.status == "completed")
        .order_by(VisitRecord.id.desc())
    ).first()

    if latest_visit is None:
        raise HTTPException(status_code=404, detail="No completed visit report available")

    property_item = session.get(PropertyRecord, latest_visit.property_id)
    if property_item is None:
        raise HTTPException(status_code=404, detail="Property not found")

    completed_sections = sorted((latest_visit.section_scores or {}).keys())
    score_values = list((latest_visit.section_scores or {}).values())
    total_score = round(sum(score_values) / len(score_values), 2) if score_values else None

    sections = [
        ReportSection(
            title="Visit summary",
            body=f"Visited on {latest_visit.visit_date}. Asking price {format_price(property_item.listing_price)}. Required sections completed: {', '.join(completed_sections) if completed_sections else 'none'}.",
        ),
        ReportSection(
            title="Top findings",
            body=(
                f"Completed sections: {', '.join(completed_sections)}. Average score {total_score}"
                if completed_sections
                else "No completed sections yet."
            ),
        ),
        ReportSection(
            title="Red flags",
            body="; ".join(latest_visit.red_flags) if latest_visit.red_flags else "No red flags recorded.",
        ),
        ReportSection(
            title="Recommendation",
            body=latest_visit.recommendation_notes or "No recommendation note recorded.",
        ),
    ]

    return VisitReportResponse(
        property_id=property_item.id,
        address=property_item.address,
        total_score=total_score,
        sections=sections,
    )
