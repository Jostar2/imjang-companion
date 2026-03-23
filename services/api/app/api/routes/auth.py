from uuid import uuid4

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from services.api.app.core.auth import get_current_user, issue_session, resolve_requested_role
from services.api.app.core.db import UserRecord, get_session
from services.api.app.schemas.auth import LoginRequest, MeResponse, SessionResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=SessionResponse)
def login(payload: LoginRequest, session: Session = Depends(get_session)) -> SessionResponse:
    normalized_email = str(payload.email).strip().lower()
    granted_role = resolve_requested_role(normalized_email, payload.role)
    user = session.scalars(select(UserRecord).where(UserRecord.email == normalized_email)).first()
    if user is None:
        user = UserRecord(
            id=f"user-{uuid4().hex[:12]}",
            email=normalized_email,
            display_name=payload.display_name.strip(),
            role=granted_role,
        )
        session.add(user)
        session.commit()
        session.refresh(user)
    else:
        user.display_name = payload.display_name.strip()
        user.role = granted_role
        session.commit()
        session.refresh(user)

    session_record = issue_session(user, session)
    return SessionResponse(
        token=session_record.token,
        user_id=user.id,
        email=user.email,
        display_name=user.display_name,
        role=user.role,
    )


@router.get("/me", response_model=MeResponse)
def me(current_user: UserRecord = Depends(get_current_user)) -> MeResponse:
    return MeResponse(
        user_id=current_user.id,
        email=current_user.email,
        display_name=current_user.display_name,
        role=current_user.role,
    )
