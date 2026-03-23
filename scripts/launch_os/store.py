from __future__ import annotations

import json
from types import SimpleNamespace
from typing import Any

from scripts.product_context import ROOT, active_run_root, load_project


def read_project_run_state(project_slug: str | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
    project = load_project()
    if project_slug and project_slug != project["slug"]:
        raise ValueError(f"Unknown project slug: {project_slug}")
    run_root = active_run_root()
    payload = json.loads((run_root / "state" / "run-state.json").read_text(encoding="utf8"))
    return SimpleNamespace(**project), payload


def build_blockers(project: dict[str, Any], run_state: dict[str, Any]) -> list[dict[str, Any]]:
    blockers: list[dict[str, Any]] = []
    task_names = list(run_state.get("blocked", []))
    for task_name in task_names:
        blockers.append(
            {
                "id": len(blockers) + 1,
                "project_slug": project.slug,
                "run_id": run_state["run_id"],
                "blocker_key": f"{project.slug}:{run_state['run_id']}:{task_name}",
                "title": task_name,
                "reason": f"Product-local blocker `{task_name}` is still open.",
                "source": "product_repo_state",
                "status": "open",
                "metadata": {"task_name": task_name},
                "created_at_utc": "",
                "updated_at_utc": "",
                "resolved_at_utc": None,
            }
        )
    return blockers


def list_active_blockers(project_slug: str) -> list[dict[str, Any]]:
    project, run_state = read_project_run_state(project_slug)
    return build_blockers(project, run_state)


def list_blockers(project_slug: str) -> list[dict[str, Any]]:
    return list_active_blockers(project_slug)


def list_open_alerts(project_slug: str) -> list[dict[str, Any]]:
    return []


def list_recent_events(project_slug: str, limit: int = 50) -> list[dict[str, Any]]:
    return []


def list_recent_attempts(project_slug: str, limit: int = 20) -> list[dict[str, Any]]:
    return []


def list_queue_items(project_slug: str) -> list[dict[str, Any]]:
    return []


def sync_project_state(project_slug: str | None = None) -> tuple[Any, dict[str, Any]]:
    return read_project_run_state(project_slug)


def get_status_payload(project_slug: str | None = None) -> dict[str, Any]:
    project, run_state = read_project_run_state(project_slug)
    blockers = build_blockers(project, run_state)
    return {
        "active_project_slug": project.slug,
        "active_run_id": run_state["run_id"],
        "run_status": run_state["status"],
        "current_phase": run_state["current_phase"],
        "next_tasks": list(run_state.get("next_tasks", [])),
        "runtime_completed": [],
        "effective_completed": list(run_state.get("completed", [])),
        "run_blocked": list(run_state.get("blocked", [])),
        "runner_state": "idle",
        "current_queue_item": None,
        "queue_counts": {
            "pending": 0,
            "leased": 0,
            "running": 0,
            "succeeded": 0,
            "failed": 0,
            "blocked": 0,
            "canceled": 0,
        },
        "open_blocker_count": len(blockers),
        "blockers": blockers,
        "open_alert_count": 0,
        "alerts": [],
        "human_gates": list(getattr(project, "human_gates", [])),
        "last_heartbeat_utc": None,
        "last_error": None,
    }


def pause_runner(project_slug: str) -> dict[str, Any]:
    return {"state": "paused"}


def resume_runner(project_slug: str) -> dict[str, Any]:
    return {"state": "idle"}


def retry_queue_item(project_slug: str, queue_item_id: int) -> dict[str, Any]:
    raise ValueError("Launch OS runtime queue is not embedded in the standalone product repo.")


def acknowledge_blocker(project_slug: str, blocker_id: int, note: str = "") -> dict[str, Any]:
    blockers = list_active_blockers(project_slug)
    for blocker in blockers:
        if blocker["id"] == blocker_id:
            return blocker
    raise ValueError(f"Blocker not found: {blocker_id}")


def acknowledge_alert(project_slug: str, alert_id: int) -> dict[str, Any]:
    raise ValueError(f"Alert not found: {alert_id}")


def write_snapshots(project_slug: str | None = None) -> None:
    return None
