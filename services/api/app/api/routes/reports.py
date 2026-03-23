from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from services.api.app.core.auth import get_current_user, require_global_scope, require_owner_resource_access
from services.api.app.core.db import ProjectRecord, PropertyRecord, UserRecord, VisitRecord, get_session
from services.api.app.schemas.report import ComparisonEntry, ComparisonResponse, ReportSection, VisitReportResponse

router = APIRouter(prefix="/reports", tags=["reports"])


def format_price(value: int | None) -> str:
    if value is None:
        return "TBD"
    return f"{value:,} KRW"


def resolve_target_owner_user_id(current_user: UserRecord, owner_user_id: str | None) -> str:
    if owner_user_id is not None:
        require_global_scope("all", current_user)
        return owner_user_id
    return current_user.id


def resolve_project(
    *,
    session: Session,
    current_user: UserRecord,
    project_id: str | None,
    owner_user_id: str | None,
) -> ProjectRecord:
    target_owner_user_id = resolve_target_owner_user_id(current_user, owner_user_id)

    if project_id is not None:
        project = session.get(ProjectRecord, project_id)
        if project is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        require_owner_resource_access(current_user, project.owner_user_id, detail="Project not found")
        if project.owner_user_id != target_owner_user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        return project

    projects = session.scalars(
        select(ProjectRecord)
        .where(ProjectRecord.owner_user_id == target_owner_user_id)
        .order_by(ProjectRecord.name.asc(), ProjectRecord.id.asc())
    ).all()
    if not projects:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No project found")
    if len(projects) > 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="project_id is required when multiple projects exist",
        )
    return projects[0]


def latest_relevant_visit(session: Session, property_id: str) -> VisitRecord | None:
    latest_completed = session.scalars(
        select(VisitRecord)
        .where(VisitRecord.property_id == property_id, VisitRecord.status == "completed")
        .order_by(VisitRecord.visit_date.desc(), VisitRecord.id.desc())
    ).first()
    if latest_completed is not None:
        return latest_completed

    return session.scalars(
        select(VisitRecord)
        .where(VisitRecord.property_id == property_id)
        .order_by(VisitRecord.visit_date.desc(), VisitRecord.id.desc())
    ).first()


def load_report_visit(
    *,
    session: Session,
    project: ProjectRecord,
) -> VisitRecord:
    latest_visit = session.scalars(
        select(VisitRecord)
        .join(PropertyRecord, VisitRecord.property_id == PropertyRecord.id)
        .where(PropertyRecord.project_id == project.id, VisitRecord.status == "completed")
        .order_by(VisitRecord.visit_date.desc(), VisitRecord.id.desc())
    ).first()
    if latest_visit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No completed visit report available")
    return latest_visit


@router.get("/comparison", response_model=ComparisonResponse)
def comparison(
    project_id: str | None = None,
    owner_user_id: str | None = None,
    session: Session = Depends(get_session),
    current_user: UserRecord = Depends(get_current_user),
) -> ComparisonResponse:
    project = resolve_project(
        session=session,
        current_user=current_user,
        project_id=project_id,
        owner_user_id=owner_user_id,
    )

    properties = session.scalars(
        select(PropertyRecord)
        .where(PropertyRecord.project_id == project.id)
        .order_by(PropertyRecord.id)
    ).all()

    entries: list[ComparisonEntry] = []
    for property_item in properties:
        latest_visit = latest_relevant_visit(session, property_item.id)
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
                visit_id=latest_visit.id if latest_visit else None,
                visit_date=latest_visit.visit_date if latest_visit else None,
                visit_status=latest_visit.status if latest_visit else None,
                strengths=strengths,
                red_flags=red_flags,
            )
        )

    return ComparisonResponse(
        project_count=1,
        project_id=project.id,
        project_name=project.name,
        property_count=len(entries),
        entries=entries,
    )


@router.get("/latest", response_model=VisitReportResponse)
def latest_report(
    project_id: str | None = None,
    visit_id: str | None = None,
    owner_user_id: str | None = None,
    session: Session = Depends(get_session),
    current_user: UserRecord = Depends(get_current_user),
) -> VisitReportResponse:
    target_owner_user_id = resolve_target_owner_user_id(current_user, owner_user_id)
    if visit_id is not None:
        latest_visit = session.get(VisitRecord, visit_id)
        if latest_visit is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visit not found")
        property_item = session.get(PropertyRecord, latest_visit.property_id)
        project = session.get(ProjectRecord, property_item.project_id) if property_item else None
        if property_item is None or project is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visit not found")
        require_owner_resource_access(current_user, project.owner_user_id, detail="Visit not found")
        if project.owner_user_id != target_owner_user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visit not found")
        if project_id is not None and project.id != project_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visit not found")
        if latest_visit.status != "completed":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Visit report requires a completed visit")
    else:
        project = resolve_project(
            session=session,
            current_user=current_user,
            project_id=project_id,
            owner_user_id=owner_user_id,
        )
        latest_visit = load_report_visit(
            session=session,
            project=project,
        )

    property_item = session.get(PropertyRecord, latest_visit.property_id)
    if property_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")

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
        project_id=project.id,
        project_name=project.name,
        visit_id=latest_visit.id,
        visit_date=latest_visit.visit_date,
        property_id=property_item.id,
        address=property_item.address,
        total_score=total_score,
        sections=sections,
    )
