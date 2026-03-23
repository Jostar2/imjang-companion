from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from services.api.app.core.auth import get_current_user, require_global_scope, require_owner_resource_access
from services.api.app.core.db import ProjectRecord, UserRecord, get_session
from services.api.app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from services.api.app.services.resource_cleanup import delete_project_storage

router = APIRouter(prefix="/projects", tags=["projects"])


def serialize_project(project: ProjectRecord) -> ProjectResponse:
    return ProjectResponse(
        id=project.id,
        owner_user_id=project.owner_user_id,
        name=project.name,
        region=project.region,
        budget=project.budget,
        notes=project.notes,
    )


@router.get("", response_model=list[ProjectResponse])
def list_projects(
    scope: str = Query(default="owned", pattern="^(owned|all)$"),
    session: Session = Depends(get_session),
    current_user: UserRecord = Depends(get_current_user),
) -> list[ProjectResponse]:
    require_global_scope(scope, current_user)
    query = select(ProjectRecord).order_by(ProjectRecord.id)
    if scope == "owned":
        query = query.where(ProjectRecord.owner_user_id == current_user.id)
    projects = session.scalars(query).all()
    return [serialize_project(project) for project in projects]


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    payload: ProjectCreate,
    session: Session = Depends(get_session),
    current_user: UserRecord = Depends(get_current_user),
) -> ProjectResponse:
    project = ProjectRecord(
        id=f"project-{uuid4().hex[:12]}",
        owner_user_id=current_user.id,
        name=payload.name.strip(),
        region=payload.region.strip() if payload.region else None,
        budget=payload.budget.strip() if payload.budget else None,
        notes=payload.notes,
    )
    session.add(project)
    session.commit()
    session.refresh(project)
    return serialize_project(project)


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: str,
    session: Session = Depends(get_session),
    current_user: UserRecord = Depends(get_current_user),
) -> ProjectResponse:
    project = session.get(ProjectRecord, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    require_owner_resource_access(current_user, project.owner_user_id, detail="Project not found")

    return serialize_project(project)


@router.patch("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: str,
    payload: ProjectUpdate,
    session: Session = Depends(get_session),
    current_user: UserRecord = Depends(get_current_user),
) -> ProjectResponse:
    project = session.get(ProjectRecord, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    require_owner_resource_access(current_user, project.owner_user_id, detail="Project not found")

    changes = payload.model_dump(exclude_unset=True)
    if "name" in changes and changes["name"] is not None:
        project.name = changes["name"].strip()
    if "region" in changes:
        project.region = changes["region"].strip() if changes["region"] else None
    if "budget" in changes:
        project.budget = changes["budget"].strip() if changes["budget"] else None
    if "notes" in changes:
        project.notes = changes["notes"]

    session.commit()
    session.refresh(project)
    return serialize_project(project)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_project(
    project_id: str,
    session: Session = Depends(get_session),
    current_user: UserRecord = Depends(get_current_user),
) -> Response:
    project = session.get(ProjectRecord, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    require_owner_resource_access(current_user, project.owner_user_id, detail="Project not found")

    delete_project_storage(project)
    session.delete(project)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
