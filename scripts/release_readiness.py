from __future__ import annotations

import argparse
import json
import sys

from scripts.product_context import ROOT, active_run_root, release_checklist_path


def main() -> int:
    argparse.ArgumentParser(description="Validate release-readiness artifacts for Imjang Companion.").parse_args()
    run_dir = active_run_root()

    required_files = [
        run_dir / "PRD.md",
        run_dir / "ADR-001.md",
        run_dir / "acceptance.yaml",
        run_dir / "task-graph.json",
        run_dir / "qa" / "regression-matrix.md",
        run_dir / "qa" / "smoke-plan.md",
        run_dir / "release-notes.md",
        release_checklist_path(),
    ]

    missing = [str(path.relative_to(ROOT)) for path in required_files if not path.exists()]
    if missing:
        print("Missing release artifacts:")
        for path in missing:
            print(f"- {path}")
        return 1

    state = json.loads((run_dir / "state" / "run-state.json").read_text(encoding="utf8"))
    print("Project: imjang-companion")
    print(f"Run path: {run_dir.relative_to(ROOT)}")
    print(f"Run status: {state['status']}")
    print(f"Current phase: {state['current_phase']}")
    print("Next tasks:")
    for task in state["next_tasks"]:
        print(f"- {task}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
