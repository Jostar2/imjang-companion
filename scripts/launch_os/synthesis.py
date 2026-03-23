from __future__ import annotations

from typing import Any


def build_synthesis_snapshot(context: dict[str, Any], run_state: dict[str, Any]) -> dict[str, Any]:
    return {
        "active_project_slug": context["slug"],
        "active_run_id": run_state["run_id"],
        "run_status": run_state["status"],
        "current_phase": run_state["current_phase"],
        "completed": list(run_state.get("completed", [])),
        "next_tasks": list(run_state.get("next_tasks", [])),
        "queue_candidates": [],
    }
