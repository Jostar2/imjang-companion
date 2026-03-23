# Regression Matrix

## Scope
Core visit flow (AC-001 to AC-006) for `run-001-real-estate-imjang`, covering the happy path plus key regressions tied to the latest acceptance and non-goals.

## Matrix

| Case ID | Acceptance | Scenario | Evidence type | Steps / Checks | Expected outcome |
|---|---|---|---|---|---|
| RM-001 | AC-001 | Create project and multiple properties | ui_smoke | 1) create a project 2) create 2 properties under project | All resources created and listed under the same project |
| RM-002 | AC-001 | Parent/child consistency | unit_test | create property with missing/invalid `project_id` | API rejects with validation error; no orphaned property created |
| RM-003 | AC-002 | Required checklist enforcement | api_test | create visit draft, submit completion request with incomplete required sections | API rejects completion and keeps visit status as `draft` |
| RM-004 | AC-002 | Completion gate success path | ui_smoke, api_test | fill required sections (`property`, `building`, `neighborhood`) then mark complete | visit status transitions to `completed` only after required sections |
| RM-005 | AC-003 | Notes and scores persist on visit | api_test | update visit with section scores + notes; fetch visit | section payload mirrors input and score aggregate updates consistently |
| RM-006 | AC-003 | Attachment links to correct visit | api_test, manual_check | upload attachment in one visit and fetch related visits | attachment metadata remains tied to that visit only |
| RM-007 | AC-003 | Upload failure recovery | manual_check | simulate upload error for one file, keep visit draft | failed attachment remains retryable and visit data remains saved |
| RM-008 | AC-004 | Comparison coverage (>=2 properties) | ui_smoke | complete visits for at least 2 properties and open comparison | comparison view displays both properties, total score, red flags |
| RM-009 | AC-004 | Score regression under edits | manual_check | edit a section score after completion and refresh comparison | score and red-flag ranking update in line with latest payload |
| RM-010 | AC-005 | Report content completeness | ui_smoke | open report for project with at least one completed visit | report includes visit date, key findings, recommendation notes, red flags |
| RM-011 | AC-006 | Browser refresh restore | manual_check | enter checklist/notes, refresh browser, confirm same draft loaded | in-progress draft restored with partial data (same device/browser session only) |
| RM-012 | AC-006 | Draft clear/submit semantics | manual_check | submit visit or clear draft, then refresh | restored draft is removed after submit/explicit clear |
| RM-013 | AC-006 | Cross-device non-support is respected | manual_check | continue on different device/browser | draft is not restored (documented non-goal) |
| RM-014 | AC-001/003/004/005 | Deletion cleanup regression | manual_check | delete a project/property used in smoke test | dependent child resources removed; no stale visits/attachments remain |

## Regression focus notes

- Keep checklist taxonomy stable across required-field validation for this slice (section names and required flags).
- Any change to attachment upload error handling should be smoke-verified with retry paths.
- Autosave persistence is intentionally browser-local; do not treat cross-device sync as scope regression in v1.
- Mark these scenarios as **pass required** before `INF-001` proceeds:
  - RM-003, RM-004, RM-006, RM-008, RM-010, RM-011, RM-012

## Evidence ownership

- api tests: `services/api/tests/test_visits.py`
- UI path checks: `apps/web/src/app/**`
- Manual checks: browser smoke run against local or staging frontend
- Automation path: `scripts/smoke_check.py --base-url <API_URL> --include-attachment`
