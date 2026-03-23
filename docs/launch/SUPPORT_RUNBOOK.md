# Support Runbook

## Support scope for v1

- project or property creation issues
- draft restore confusion
- attachment upload failures and retry flow
- comparison/report data mismatch

## Severity levels

- `SEV-1`
  - visit completion blocked
  - saved data appears missing
  - auth or ownership boundary broken
- `SEV-2`
  - attachment retry failing
  - comparison/report not reflecting the latest saved visit
  - repeated autosave restore confusion during pilot onboarding
- `SEV-3`
  - copy confusion
  - non-blocking formatting issues
  - launch collateral mismatch

## First-response checklist

1. confirm environment: local, staging, or pilot
2. identify project and property involved
3. confirm whether the issue blocks visit completion or only affects read surfaces
4. check whether the issue is reproducible after refresh
5. if attachment-related, confirm whether the visit itself was saved

## Evidence to capture before escalation

- user email or pilot account
- project name and `project_id`
- property address and `property_id`
- `visit_id` if the issue touches report, autosave, or attachment upload
- screenshot or short screen recording
- browser and device
- exact timestamp of the failure

## Known behaviors

- V1 is online-first. Draft restore is same-browser only.
- Draft restore does not recover binary files.
- Attachment upload may fail independently from visit save.
- Comparison and report should reflect stored visit data, not memory-only notes.

## Response templates

### Draft restore confusion

Use:

> The visit draft can restore in the same browser on the same device. It restores section notes and scores, but it does not restore binary photo files. Let us confirm whether the visit itself was already saved on the server.

### Attachment failure with saved visit

Use:

> The visit record should still be saved even if the file upload failed. We will confirm the saved visit first, then retry the attachment separately so the rest of the diligence notes are not lost.

### Comparison/report mismatch

Use:

> Comparison and report read from the latest saved visit data inside one project. We are checking the exact project, property, and visit that should have been used for this summary.

## Escalation rules

- capture-flow regression: escalate immediately
- auth or ownership regression: escalate immediately
- report wording polish: batch unless it blocks pilot conversion
- human gates around pricing, secrets, legal, or production: do not answer autonomously

## Rollback triggers

- any `SEV-1` issue reproduced in staging
- report/comparison reads from the wrong project
- attachment save failure causes the visit itself to disappear
