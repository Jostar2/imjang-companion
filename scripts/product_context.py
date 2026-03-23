from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT_PATH = ROOT / "project.json"


def load_project() -> dict:
    return json.loads(PROJECT_PATH.read_text(encoding="utf8"))


def active_run_root() -> Path:
    project = load_project()
    return ROOT / project["paths"]["active_run_root"]


def release_checklist_path() -> Path:
    project = load_project()
    return ROOT / project["documents"]["release_checklist"]
