# Release Strategy

## Release objective

The first staging-ready release must prove one authenticated user can:

- create a project
- add at least two properties to that project
- complete a visit with required checklist sections
- recover an in-progress draft after refresh in the same browser
- preserve the saved visit even when attachment upload needs a retry
- compare project properties from stored visit evidence
- review a report generated from a completed visit

## Release unit

The releasable unit is one bounded workflow:

`project -> property -> visit -> attachment evidence -> comparison/report projection`

The release prioritizes capture integrity over downstream read surfaces. If comparison or report becomes unstable, capture remains the protected path.

## Sequencing

1. Domain contract freeze
   - Inputs: `ADR-001.md`, `acceptance.yaml`
   - Gate: project/property/visit/checklist/report seams are explicit, and the v1 checklist taxonomy is frozen.

2. Capture foundation
   - Tasks: `BE-001`, `FE-001`
   - Goal: owner-scoped project/property CRUD and mobile workspace navigation.
   - Gate: project and property create/list flows are stable.

3. Visit completion path
   - Tasks: `BE-002`, `FE-002`
   - Goal: visit creation, checklist persistence, completion blocking, browser-local autosave, and attachment retry handling.
   - Gate: required sections block completion; saved visit data survives attachment upload failures.

4. Read projections
   - Tasks: `FE-003` plus any report-contract alignment needed within the existing API boundary
   - Goal: comparison and report surfaces reflect project- or visit-scoped data instead of owner-wide placeholders.
   - Gate: comparison and report behavior matches the product workflow boundary defined in the ADR.

5. Quality and release prep
   - Tasks: `QA-001`, `INF-001`
   - Goal: smoke/regression coverage, storage-path validation, release notes, and checklist completion.
   - Gate: staging smoke plan includes autosave restore, upload retry, comparison, and report review.

6. Human-controlled promotion
   - Required gates: secret population, pricing go-live, legal or compliance claims, production approval.
   - Rule: no production-ready claim until those human gates are explicitly cleared.

## Verification expectations

- `document_review` for architecture outputs
- `npm run api:test`
- `npm run api:check`
- `npm run web:lint`
- `npm run web:build`
- manual or smoke validation for:
  - draft restore after refresh
  - attachment upload retry
  - two-property comparison within one project
  - report rendering from a completed visit

## Rollback posture

### Level 1: comparison or report regression

- Hide `/comparison` and `/report` user routes.
- Keep project/property/visit capture available.
- Do not change visit persistence semantics during the rollback.

### Level 2: attachment path instability

- Disable attachment upload entry points and keep note/score capture active.
- Preserve visit completion for text-only evidence if the release decision requires it.
- Validate storage cleanup before re-enabling uploads.

### Level 3: checklist contract regression

- Block the release candidate.
- Revert to the last known stable checklist key set rather than partially changing completion logic.
- Re-run visit completion regression before promotion resumes.

### Level 4: auth or ownership regression

- Stop promotion entirely.
- Do not widen roles or share access as a release workaround.
- Escalate to architect plus human review because the change crosses a protected boundary.

## Explicit non-goals for this release

- pricing automation or billing changes
- collaborator permissions or public share links
- offline queueing or offline attachment upload
- PDF export or persisted report snapshots
- production deployment without human approval
