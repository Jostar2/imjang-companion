# Smoke Plan

## Objective
Validate the core visit flow in one pass (creation -> completion -> comparison -> report) and capture API + UI evidence that supports QA-001 sign-off.

## Environment
- Local stack (`http://localhost:8000`, running API and web)
- Staging API/base URL for pre-release checks
- Browser: mobile viewport at minimum (MVP requirement)

## Automated API smoke (minimum required)

Run command:

```bash
python scripts/smoke_check.py --base-url <API_URL> --include-attachment
```

Expected outputs:
- `health` endpoint success
- visit creation and completion succeed with required sections
- `visit.status == "completed"` after smoke payload submits with required fields
- attachment upload returns size metadata equal to payload for the binary smoke fixture

### Failure handling (API smoke)
- If the script exits with `smoke-failed`, preserve stdout/stderr with timestamp as evidence.
- Fix root cause only for items in RM-001~RM-006 or re-run command after corrective changes.
- A green run is required before manual browser smoke.

## Manual browser smoke (staging/local UI verification)

1. Authenticate as a buyer user and open the app home/project page.
2. Create one project with a unique name (store timestamp in notes).
3. Add at least two properties under the project.
4. Open visit for Property A and save partial checklist data.
5. Refresh the same browser tab and confirm draft values restore (autosave restore).
6. Finish all required checklist sections and mark Property A visit complete.
7. Repeat visit for Property B through completion (same required sections minimum).
8. Open comparison view and confirm aggregate score and red-flag summary include both properties.
9. Open report and verify: visit date, key findings, red flags, recommendation notes.
10. Simulate failed attachment upload and verify only failed attachment is retryable while other visit data remains persisted.
11. Submit/clear visit draft and refresh to confirm draft no longer restores for completed/cleared state.

### Pass/Fail gates
- Any hard error toast/crash in each step fails the run.
- If RM-012 state restoration rule fails, block progression and classify as severity-2 regression.
- If comparison misses any completed property in step 8, block progression and classify as severity-1 regression.
- If report misses required fields (date/findings/red flags/recommendation), block progression and classify as severity-1 regression.

## Evidence capture
- Capture screenshots for steps 5, 8, and 9.
- Attach API log for automated smoke command.
- Save request/response snippets for at least:
  - project create
  - first visit create
  - first completed visit payload
  - report query response

## Exit criteria for QA-001 closure
- Automated smoke passes once in local and once in staging context.
- Manual browser smoke executes all 11 steps with zero blockers.
- Every AC-001 to AC-006 has at least one corresponding pass observation in the matrix and this smoke plan.
