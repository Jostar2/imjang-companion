from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from services.api.app.core.auth import get_current_user, require_global_scope, require_owner_resource_access
from services.api.app.core.db import ProjectRecord, PropertyRecord, UserRecord, get_session
from services.api.app.schemas.property import PropertyCreate, PropertyResponse, PropertyUpdate

router = APIRouter(prefix="/properties", tags=["properties"])


def serialize_property(property_item: PropertyRecord) -> PropertyResponse:
    owner_user_id = property_item.project.owner_user_id if property_item.project else None
    return PropertyResponse(
        id=property_item.id,
        project_id=property_item.project_id,
        owner_user_id=owner_user_id,
        address=property_item.address,
        listing_price=property_item.listing_price,
        property_type=property_item.property_type,
        source=property_item.source,
    )


@router.get("", response_model=list[PropertyResponse])
def list_properties(
    project_id: str | None = None,
    scope: str = Query(default="owned", pattern="^(owned|all)$"),
    session: Session = Depends(get_session),
    current_user: UserRecord = Depends(get_current_user),
) -> list[PropertyResponse]:
    require_global_scope(scope, current_user)
    query = select(PropertyRecord).join(ProjectRecord, PropertyRecord.project_id == ProjectRecord.id).order_by(PropertyRecord.id)
    if scope == "owned":
        query = query.where(ProjectRecord.owner_user_id == current_user.id)
    if project_id is not None:
        query = query.where(PropertyRecord.project_id == project_id)
    properties = session.scalars(query).all()
    return [serialize_property(property_item) for property_item in properties]


@router.post("", response_model=PropertyResponse, status_code=status.HTTP_201_CREATED)
def create_property(
    payload: PropertyCreate,
    session: Session = Depends(get_session),
    current_user: UserRecord = Depends(get_current_user),
) -> PropertyResponse:
    project = session.get(ProjectRecord, payload.project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    require_owner_resource_access(current_user, project.owner_user_id, detail="Project not found")

    property_item = PropertyRecord(
        id=f"property-{uuid4().hex[:12]}",
        project_id=payload.project_id,
        address=payload.address.strip(),
        listing_price=payload.listing_price,
        property_type=payload.property_type,
        source=payload.source.strip() if payload.source else None,
    )
    session.add(property_item)
    session.commit()
    session.refresh(property_item)
    return serialize_property(property_item)


@router.get("/{property_id}", response_model=PropertyResponse)
def get_property(
    property_id: str,
    session: Session = Depends(get_session),
    current_user: UserRecord = Depends(get_current_user),
) -> PropertyResponse:
    property_item = session.get(PropertyRecord, property_id)
    if property_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    project = session.get(ProjectRecord, property_item.project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    require_owner_resource_access(current_user, project.owner_user_id, detail="Property not found")
    return serialize_property(property_item)


@router.patch("/{property_id}", response_model=PropertyResponse)
def update_property(
    property_id: str,
    payload: PropertyUpdate,
    session: Session = Depends(get_session),
    current_user: UserRecord = Depends(get_current_user),
) -> PropertyResponse:
    property_item = session.get(PropertyRecord, property_id)
    if property_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    project = session.get(ProjectRecord, property_item.project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    require_owner_resource_access(current_user, project.owner_user_id, detail="Property not found")

    changes = payload.model_dump(exclude_unset=True)
    if "address" in changes and changes["address"] is not None:
        property_item.address = changes["address"].strip()
    if "listing_price" in changes:
        property_item.listing_price = changes["listing_price"]
    if "property_type" in changes:
        property_item.property_type = changes["property_type"]
    if "source" in changes:
        property_item.source = changes["source"].strip() if changes["source"] else None

    session.commit()
    session.refresh(property_item)
    return serialize_property(property_item)


@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_property(
    property_id: str,
    session: Session = Depends(get_session),
    current_user: UserRecord = Depends(get_current_user),
) -> Response:
    property_item = session.get(PropertyRecord, property_id)
    if property_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    project = session.get(ProjectRecord, property_item.project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    require_owner_resource_access(current_user, project.owner_user_id, detail="Property not found")

    session.delete(property_item)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
