from pydantic import BaseModel


class ReleaseReadinessResponse(BaseModel):
    run_status: str
    current_phase: str
    next_tasks: list[str]
    blocked: list[str]


class UserOpsSummary(BaseModel):
    user_id: str
    email: str
    display_name: str
    role: str
    project_count: int
    property_count: int
    visit_count: int


class OpsSummaryResponse(BaseModel):
    total_users: int
    total_projects: int
    total_properties: int
    total_visits: int
    total_completed_visits: int
    total_attachments: int
    users: list[UserOpsSummary]


class LaunchOsQueueItemResponse(BaseModel):
    id: int
    project_slug: str
    run_id: str
    queue_key: str
    label: str
    owner_agent: str
    status: str
    priority: int
    source: str
    payload: dict[str, object]
    attempt_count: int
    last_error: str | None
    created_at_utc: str
    updated_at_utc: str
    available_at_utc: str | None
    leased_at_utc: str | None
    finished_at_utc: str | None


class LaunchOsBlockerResponse(BaseModel):
    id: int
    project_slug: str
    run_id: str
    blocker_key: str
    title: str
    reason: str
    source: str
    status: str
    metadata: dict[str, object]
    created_at_utc: str
    updated_at_utc: str
    resolved_at_utc: str | None


class LaunchOsAlertResponse(BaseModel):
    id: int
    project_slug: str
    queue_item_id: int | None
    blocker_id: int | None
    severity: str
    status: str
    title: str
    message: str
    source: str
    metadata: dict[str, object]
    created_at_utc: str
    updated_at_utc: str
    resolved_at_utc: str | None


class LaunchOsEventResponse(BaseModel):
    id: int
    project_slug: str
    queue_item_id: int | None
    blocker_id: int | None
    kind: str
    message: str
    metadata: dict[str, object]
    created_at_utc: str


class LaunchOsAttemptResponse(BaseModel):
    attempt_id: int
    queue_item_id: int
    label: str
    agent_role: str
    result_status: str
    exit_code: int | None
    summary: str | None
    structured_summary: dict[str, object]
    started_at_utc: str
    finished_at_utc: str | None


class LaunchOsStatusResponse(BaseModel):
    active_project_slug: str
    active_run_id: str
    run_status: str
    current_phase: str
    next_tasks: list[str]
    runtime_completed: list[str]
    effective_completed: list[str]
    run_blocked: list[str]
    runner_state: str
    current_queue_item: LaunchOsQueueItemResponse | None
    queue_counts: dict[str, int]
    open_blocker_count: int
    blockers: list[LaunchOsBlockerResponse]
    open_alert_count: int
    alerts: list[LaunchOsAlertResponse]
    human_gates: list[str]
    last_heartbeat_utc: str | None
    last_error: str | None


class LaunchOsControlResponse(BaseModel):
    ok: bool
    runner_state: str
    message: str


class LaunchOsSynthesisCandidateResponse(BaseModel):
    queue_key: str
    label: str
    owner_agent: str
    source: str
    priority: int
    payload: dict[str, object]


class LaunchOsSynthesisResponse(BaseModel):
    active_project_slug: str
    active_run_id: str
    run_status: str
    current_phase: str
    completed: list[str]
    next_tasks: list[str]
    queue_candidates: list[LaunchOsSynthesisCandidateResponse]
