from statistics import mean
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from services.api.app.core.auth import get_current_user, require_global_scope, require_owner_resource_access
from services.api.app.core.db import AttachmentRecord, ProjectRecord, PropertyRecord, UserRecord, VisitRecord, get_session
from services.api.app.schemas.attachment import AttachmentResponse
from services.api.app.schemas.visit import VisitCreate, VisitResponse, VisitUpdate
from services.api.app.services.storage import storage_service

router = APIRouter(prefix="/visits", tags=["visits"])

REQUIRED_SECTIONS = ("property", "building", "neighborhood")


def serialize_attachment(attachment: AttachmentRecord) -> AttachmentResponse:
    return AttachmentResponse(
        id=attachment.id,
        visit_id=attachment.visit_id,
        filename=attachment.filename,
        content_type=attachment.content_type,
        category=attachment.category,
        storage_backend=attachment.storage_backend,
        storage_key=attachment.storage_key,
        size_bytes=attachment.size_bytes,
    )


def serialize_visit(visit: VisitRecord) -> VisitResponse:
    owner_user_id = None
    if visit.property and visit.property.project:
        owner_user_id = visit.property.project.owner_user_id
    missing_sections = [section for section in REQUIRED_SECTIONS if section not in (visit.section_scores or {})]
    scores = list((visit.section_scores or {}).values())
    total_score = round(mean(scores), 2) if scores else None
    attachments = [serialize_attachment(attachment) for attachment in visit.attachments]

    return VisitResponse(
        id=visit.id,
        property_id=visit.property_id,
        owner_user_id=owner_user_id,
        visit_date=visit.visit_date,
        status=visit.status,
        completed_sections=sorted((visit.section_scores or {}).keys()),
        missing_sections=missing_sections,
        total_score=total_score,
        red_flags=visit.red_flags or [],
        recommendation_notes=visit.recommendation_notes,
        attachments=attachments,
    )


@router.get("", response_model=list[VisitResponse])
def list_visits(
    property_id: str | None = None,
    scope: str = Query(default="owned", pattern="^(owned|all)$"),
    session: Session = Depends(get_session),
    current_user: UserRecord = Depends(get_current_user),
) -> list[VisitResponse]:
    require_global_scope(scope, current_user)
    query = (
        select(VisitRecord)
        .join(PropertyRecord, VisitRecord.property_id == PropertyRecord.id)
        .join(ProjectRecord, PropertyRecord.project_id == ProjectRecord.id)
        .order_by(VisitRecord.id)
    )
    if scope == "owned":
        query = query.where(ProjectRecord.owner_user_id == current_user.id)
    if property_id is not None:
        query = query.where(VisitRecord.property_id == property_id)
    visits = session.scalars(query).all()
    return [serialize_visit(visit) for visit in visits]


@router.post("", response_model=VisitResponse, status_code=status.HTTP_201_CREATED)
def create_visit(
    payload: VisitCreate,
    session: Session = Depends(get_session),
    current_user: UserRecord = Depends(get_current_user),
) -> VisitResponse:
    property_item = session.get(PropertyRecord, payload.property_id)
    if property_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    project = session.get(ProjectRecord, property_item.project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    require_owner_resource_access(current_user, project.owner_user_id, detail="Property not found")

    visit = VisitRecord(
        id=f"visit-{uuid4().hex[:12]}",
        property_id=payload.property_id,
        visit_date=payload.visit_date,
        status="draft",
        red_flags=[],
        section_scores={},
        section_notes={},
    )
    session.add(visit)
    session.commit()
    session.refresh(visit)
    return serialize_visit(visit)


@router.get("/{visit_id}", response_model=VisitResponse)
def get_visit(
    visit_id: str,
    session: Session = Depends(get_session),
    current_user: UserRecord = Depends(get_current_user),
) -> VisitResponse:
    visit = session.get(VisitRecord, visit_id)
    if visit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visit not found")
    property_item = session.get(PropertyRecord, visit.property_id)
    project = session.get(ProjectRecord, property_item.project_id) if property_item else None
    if property_item is None or project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visit not found")
    require_owner_resource_access(current_user, project.owner_user_id, detail="Visit not found")

    return serialize_visit(visit)


@router.patch("/{visit_id}", response_model=VisitResponse)
def update_visit(
    visit_id: str,
    payload: VisitUpdate,
    session: Session = Depends(get_session),
    current_user: UserRecord = Depends(get_current_user),
) -> VisitResponse:
    visit = session.get(VisitRecord, visit_id)
    if visit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visit not found")
    property_item = session.get(PropertyRecord, visit.property_id)
    project = session.get(ProjectRecord, property_item.project_id) if property_item else None
    if property_item is None or project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visit not found")
    require_owner_resource_access(current_user, project.owner_user_id, detail="Visit not found")

    fields_set = payload.model_fields_set
    section_scores = dict(visit.section_scores or {})
    section_notes = dict(visit.section_notes or {})

    for section in payload.sections:
        section_scores[section.section_name] = section.score
        section_notes[section.section_name] = section.note

    visit.section_scores = section_scores
    visit.section_notes = section_notes

    if "red_flags" in fields_set:
        visit.red_flags = payload.red_flags

    if "recommendation_notes" in fields_set:
        visit.recommendation_notes = payload.recommendation_notes

    for attachment_input in payload.attachments:
        attachment = AttachmentRecord(
            id=f"attachment-{uuid4().hex[:12]}",
            visit_id=visit.id,
            filename=attachment_input.filename,
            content_type=attachment_input.content_type,
            category=attachment_input.category,
            storage_backend="inline",
            storage_key="",
            size_bytes=0,
        )
        session.add(attachment)

    missing_sections = [section for section in REQUIRED_SECTIONS if section not in section_scores]
    if payload.mark_complete:
        if missing_sections:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Required sections are incomplete: {', '.join(missing_sections)}",
            )
        visit.status = "completed"

    session.commit()
    session.refresh(visit)
    return serialize_visit(visit)


@router.post("/{visit_id}/attachments/upload", response_model=AttachmentResponse, status_code=status.HTTP_201_CREATED)
async def upload_attachment(
    visit_id: str,
    category: str = Form(...),
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    current_user: UserRecord = Depends(get_current_user),
) -> AttachmentResponse:
    visit = session.get(VisitRecord, visit_id)
    if visit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visit not found")
    property_item = session.get(PropertyRecord, visit.property_id)
    project = session.get(ProjectRecord, property_item.project_id) if property_item else None
    if property_item is None or project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visit not found")
    require_owner_resource_access(current_user, project.owner_user_id, detail="Visit not found")

    attachment_id = f"attachment-{uuid4().hex[:12]}"
    content = await file.read()
    safe_name = (file.filename or "upload.bin").replace(" ", "-")
    stored = storage_service.save_bytes(
        visit_id=visit_id,
        attachment_id=attachment_id,
        filename=file.filename or "upload.bin",
        content=content,
    )

    attachment = AttachmentRecord(
        id=attachment_id,
        visit_id=visit_id,
        filename=safe_name,
        content_type=file.content_type or "application/octet-stream",
        category=category,
        storage_backend=stored.storage_backend,
        storage_key=stored.storage_key,
        size_bytes=stored.size_bytes,
    )
    session.add(attachment)
    session.commit()
    session.refresh(attachment)
    return serialize_attachment(attachment)
