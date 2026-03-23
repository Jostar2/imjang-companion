# Scope

## Included in current v1 scope

- visit project and property CRUD
- checklist categories for property, building, neighborhood, and red flags
- note and score capture
- image attachment plumbing
- comparison summary
- report generation shell
- browser-local autosave and draft restore for an in-progress visit on the same device/browser

## Explicit non-goals for v1

- partial offline mutation queue or background replay
- offline attachment upload
- cross-device draft recovery
- listing sync
- OCR or document parsing
- collaborator permissions
- advanced analytics

## Assumptions

- visit data writes and attachment uploads require network connectivity
- browser-local autosave is best-effort draft recovery, not the system of record
- the staged MVP remains single-user and online-first

## Success boundary

The current launch scope is successful if a single user can create a project, log two property visits, compare them, review a summary report in staging, and recover an in-progress visit draft after a browser refresh on the same device/browser.
