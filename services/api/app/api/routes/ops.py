from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from scripts.launch_os.store import (
    acknowledge_alert,
    acknowledge_blocker,
    get_status_payload,
    list_active_blockers,
    list_open_alerts,
    list_recent_attempts,
    list_blockers,
    list_queue_items,
    list_recent_events,
    pause_runner,
    read_project_run_state,
    resume_runner,
    retry_queue_item,
    sync_project_state,
    write_snapshots,
)
from scripts.launch_os.synthesis import build_synthesis_snapshot
from services.api.app.core.auth import require_admin
from services.api.app.core.db import (
    AttachmentRecord,
    ProjectRecord,
    PropertyRecord,
    UserRecord,
    VisitRecord,
    get_session,
)
from services.api.app.schemas.ops import (
    LaunchOsAttemptResponse,
    LaunchOsAlertResponse,
    LaunchOsBlockerResponse,
    LaunchOsControlResponse,
    LaunchOsEventResponse,
    LaunchOsQueueItemResponse,
    LaunchOsStatusResponse,
    LaunchOsSynthesisResponse,
    OpsSummaryResponse,
    ReleaseReadinessResponse,
    UserOpsSummary,
)

router = APIRouter(prefix="/ops", tags=["ops"])


@router.get("/release-readiness", response_model=ReleaseReadinessResponse)
def release_readiness(_: object = Depends(require_admin)) -> ReleaseReadinessResponse:
    context, payload = read_project_run_state()
    blocked = list(payload.get("blocked", []))
    blocked.extend(item["title"] for item in list_active_blockers(context.slug))
    return ReleaseReadinessResponse(
        run_status=payload["status"],
        current_phase=payload["current_phase"],
        next_tasks=payload["next_tasks"],
        blocked=blocked,
    )


@router.get("/summary", response_model=OpsSummaryResponse)
def ops_summary(
    _: object = Depends(require_admin),
    session: Session = Depends(get_session),
) -> OpsSummaryResponse:
    users = session.scalars(select(UserRecord).order_by(UserRecord.email)).all()
    user_summaries: list[UserOpsSummary] = []
    total_projects = 0
    total_properties = 0
    total_visits = 0
    total_completed_visits = 0
    total_attachments = 0

    for user in users:
        project_count = len(user.projects)
        property_count = 0
        visit_count = 0
        completed_visit_count = 0
        attachment_count = 0
        for project in user.projects:
            property_count += len(project.properties)
            for property_item in project.properties:
                visit_count += len(property_item.visits)
                for visit in property_item.visits:
                    if visit.status == "completed":
                        completed_visit_count += 1
                    attachment_count += len(visit.attachments)

        total_projects += project_count
        total_properties += property_count
        total_visits += visit_count
        total_completed_visits += completed_visit_count
        total_attachments += attachment_count

        user_summaries.append(
            UserOpsSummary(
                user_id=user.id,
                email=user.email,
                display_name=user.display_name,
                role=user.role,
                project_count=project_count,
                property_count=property_count,
                visit_count=visit_count,
            )
        )

    return OpsSummaryResponse(
        total_users=len(users),
        total_projects=total_projects,
        total_properties=total_properties,
        total_visits=total_visits,
        total_completed_visits=total_completed_visits,
        total_attachments=total_attachments,
        users=user_summaries,
    )


@router.get("/launch-os/status", response_model=LaunchOsStatusResponse)
def launch_os_status(_: object = Depends(require_admin)) -> LaunchOsStatusResponse:
    context, _ = sync_project_state()
    return LaunchOsStatusResponse(**get_status_payload(context.slug))


@router.get("/launch-os/queue", response_model=list[LaunchOsQueueItemResponse])
def launch_os_queue(_: object = Depends(require_admin)) -> list[LaunchOsQueueItemResponse]:
    context, _ = sync_project_state()
    return [LaunchOsQueueItemResponse(**item) for item in list_queue_items(context.slug)]


@router.get("/launch-os/events", response_model=list[LaunchOsEventResponse])
def launch_os_events(_: object = Depends(require_admin)) -> list[LaunchOsEventResponse]:
    context, _ = sync_project_state()
    return [LaunchOsEventResponse(**item) for item in list_recent_events(context.slug)]


@router.get("/launch-os/alerts", response_model=list[LaunchOsAlertResponse])
def launch_os_alerts(_: object = Depends(require_admin)) -> list[LaunchOsAlertResponse]:
    context, _ = sync_project_state()
    return [LaunchOsAlertResponse(**item) for item in list_open_alerts(context.slug)]


@router.get("/launch-os/attempts", response_model=list[LaunchOsAttemptResponse])
def launch_os_attempts(_: object = Depends(require_admin)) -> list[LaunchOsAttemptResponse]:
    context, _ = sync_project_state()
    return [LaunchOsAttemptResponse(**item) for item in list_recent_attempts(context.slug)]


@router.get("/launch-os/blockers", response_model=list[LaunchOsBlockerResponse])
def launch_os_blockers(_: object = Depends(require_admin)) -> list[LaunchOsBlockerResponse]:
    context, _ = sync_project_state()
    return [LaunchOsBlockerResponse(**item) for item in list_blockers(context.slug)]


@router.get("/launch-os/synthesis", response_model=LaunchOsSynthesisResponse)
def launch_os_synthesis(_: object = Depends(require_admin)) -> LaunchOsSynthesisResponse:
    context, run_state = sync_project_state()
    return LaunchOsSynthesisResponse(**build_synthesis_snapshot(context, run_state))


@router.post("/launch-os/pause", response_model=LaunchOsControlResponse)
def launch_os_pause(_: object = Depends(require_admin)) -> LaunchOsControlResponse:
    context, _ = sync_project_state()
    state = pause_runner(context.slug)
    write_snapshots(context.slug)
    return LaunchOsControlResponse(ok=True, runner_state=state["state"], message="Runner paused.")


@router.post("/launch-os/resume", response_model=LaunchOsControlResponse)
def launch_os_resume(_: object = Depends(require_admin)) -> LaunchOsControlResponse:
    context, _ = sync_project_state()
    state = resume_runner(context.slug)
    write_snapshots(context.slug)
    return LaunchOsControlResponse(ok=True, runner_state=state["state"], message="Runner resumed.")


@router.post("/launch-os/queue/{queue_item_id}/retry", response_model=LaunchOsControlResponse)
def launch_os_retry(queue_item_id: int, _: object = Depends(require_admin)) -> LaunchOsControlResponse:
    context, _ = sync_project_state()
    try:
        item = retry_queue_item(context.slug, queue_item_id)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    write_snapshots(context.slug)
    return LaunchOsControlResponse(ok=True, runner_state=get_status_payload(context.slug)["runner_state"], message=f"Queued retry for {item['label']}.")


@router.post("/launch-os/blockers/{blocker_id}/ack", response_model=LaunchOsControlResponse)
def launch_os_ack_blocker(blocker_id: int, _: object = Depends(require_admin)) -> LaunchOsControlResponse:
    context, _ = sync_project_state()
    try:
        blocker = acknowledge_blocker(context.slug, blocker_id)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    write_snapshots(context.slug)
    return LaunchOsControlResponse(ok=True, runner_state=get_status_payload(context.slug)["runner_state"], message=f"Acknowledged {blocker['title']}.")


@router.post("/launch-os/alerts/{alert_id}/ack", response_model=LaunchOsControlResponse)
def launch_os_ack_alert(alert_id: int, _: object = Depends(require_admin)) -> LaunchOsControlResponse:
    context, _ = sync_project_state()
    try:
        alert = acknowledge_alert(context.slug, alert_id)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    write_snapshots(context.slug)
    return LaunchOsControlResponse(ok=True, runner_state=get_status_payload(context.slug)["runner_state"], message=f"Acknowledged {alert['title']}.")
