from __future__ import annotations

import argparse
import json
import sys

from scripts.product_context import ROOT, active_run_root, release_checklist_path


REQUIRED_COMPLETIONS = {
    "reviewer_local_pass",
    "persistent_db_integration",
    "verified_s3_storage",
}


def main() -> int:
    argparse.ArgumentParser(description="Validate governance artifacts for Imjang Companion.").parse_args()
    run_dir = active_run_root()

    required_files = [
        run_dir / "review.md",
        run_dir / "release-notes.md",
        run_dir / "qa" / "smoke-plan.md",
        release_checklist_path(),
        ROOT / "infra" / "staging" / "DEPLOYMENT.md",
        ROOT / "infra" / "production" / "DEPLOYMENT.md",
        ROOT / ".github" / "workflows" / "deploy-staging.yml",
        ROOT / ".github" / "workflows" / "production-approval.yml",
        run_dir / "state" / "run-state.json",
    ]

    missing_files = [str(path.relative_to(ROOT)) for path in required_files if not path.exists()]
    if missing_files:
        print("Missing governance artifacts:")
        for path in missing_files:
            print(f"- {path}")
        return 1

    state = json.loads((run_dir / "state" / "run-state.json").read_text(encoding="utf8"))
    completed = set(state.get("completed", []))
    missing_states = sorted(REQUIRED_COMPLETIONS - completed)
    if missing_states:
        print("Missing governance completion markers:")
        for marker in missing_states:
            print(f"- {marker}")
        return 1

    review_text = (run_dir / "review.md").read_text(encoding="utf8")
    if "must-fix" not in review_text.lower() and "release posture" not in review_text.lower():
        print("Review artifact does not contain enough release context")
        return 1

    print("release-governance-ok: imjang-companion")
    return 0


if __name__ == "__main__":
    sys.exit(main())
