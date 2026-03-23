# Support Runbook

## Support scope for v1

- project or property creation issues
- draft restore confusion
- attachment upload failures and retry flow
- comparison/report data mismatch

## First-response checklist

1. confirm environment: local, staging, or pilot
2. identify project and property involved
3. confirm whether the issue blocks visit completion or only affects read surfaces
4. check whether the issue is reproducible after refresh
5. if attachment-related, confirm whether the visit itself was saved

## Known behaviors

- V1 is online-first. Draft restore is same-browser only.
- Draft restore does not recover binary files.
- Attachment upload may fail independently from visit save.
- Comparison and report should reflect stored visit data, not memory-only notes.

## Escalation rules

- capture-flow regression: escalate immediately
- auth or ownership regression: escalate immediately
- report wording polish: batch unless it blocks pilot conversion
- human gates around pricing, secrets, legal, or production: do not answer autonomously
