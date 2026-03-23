from __future__ import annotations

from uuid import uuid4

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from services.api.app.core.config import settings
from services.api.app.core.db import SessionRecord, UserRecord, get_session


def issue_session(user: UserRecord, session: Session) -> SessionRecord:
    session_record = SessionRecord(token=f"session-{uuid4().hex}", user_id=user.id)
    session.add(session_record)
    session.commit()
    session.refresh(session_record)
    return session_record


def is_admin(user: UserRecord) -> bool:
    return user.role == "admin"


def resolve_requested_role(email: str, requested_role: str) -> str:
    normalized_email = email.strip().lower()
    if requested_role == "admin" and normalized_email in settings.allowed_admin_emails:
        return "admin"
    return "buyer"


def require_global_scope(scope: str, current_user: UserRecord) -> None:
    if scope == "all" and not is_admin(current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin scope required")


def can_view_owner_resource(current_user: UserRecord, owner_user_id: str) -> bool:
    return is_admin(current_user) or current_user.id == owner_user_id


def can_manage_owner_resource(current_user: UserRecord, owner_user_id: str) -> bool:
    return is_admin(current_user) or current_user.id == owner_user_id


def require_owner_resource_access(
    current_user: UserRecord,
    owner_user_id: str,
    *,
    detail: str,
    allow_admin: bool = True,
) -> None:
    if current_user.id == owner_user_id:
        return
    if allow_admin and is_admin(current_user):
        return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


def get_current_user(
    authorization: str | None = Header(default=None),
    session: Session = Depends(get_session),
) -> UserRecord:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")

    token = authorization.removeprefix("Bearer ").strip()
    session_record = session.get(SessionRecord, token)
    if session_record is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session token")

    user = session.get(UserRecord, session_record.user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user


def require_admin(current_user: UserRecord = Depends(get_current_user)) -> UserRecord:
    if not is_admin(current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin role required")
    return current_user
