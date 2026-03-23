# PRD

## 1. Problem statement

People doing real-estate field visits need a structured way to capture observations, compare options, and revisit decisions later. Existing workflows are fragmented, which leads to weak comparisons and forgotten risks.

## 2. Users / roles

- individual buyer
- small-scale investor
- buyer agent or repeated-use operator
- optional collaborator reviewing the report later

## 3. Goals

- convert field visits into structured, comparable records
- reduce note loss and comparison bias
- support a mobile-first visit workflow
- produce a shareable post-visit summary

## 4. Non-goals

- legal contract analysis
- live listing ingestion from external portals
- mortgage workflows
- production-grade collaboration features

## 5. Scope

### Included

- visit project creation
- candidate property registration
- field visit checklist execution
- notes, ratings, and photo capture
- browser-local autosave and draft restore for an in-progress visit
- property comparison view
- summary report generation

### Excluded

- OCR pipeline
- payment or brokerage workflows
- realtime collaboration
- partial offline submission queue or background sync
- offline attachment upload
- cross-device draft recovery beyond browser-local autosave

## 6. User flows

1. user creates a visit project and adds candidate properties
2. user opens a property during a visit and fills a structured checklist
3. user captures notes, scores, and photos
4. user refreshes or reopens the page and can recover an in-progress draft in the same browser
5. user compares visited properties
6. user generates a summary report and reviews top risks

## 7. Functional requirements

- FR-01: create, edit, and archive visit projects
- FR-02: create, edit, and archive candidate properties
- FR-03: run a structured checklist per property visit
- FR-04: attach notes, numeric scores, and photos to a visit
- FR-05: compute a simple aggregate score per property
- FR-06: show a comparison view across properties in the same project
- FR-07: generate a summary report with highlights and red flags
- FR-08: autosave an in-progress visit draft locally in the browser and restore it on reload on the same device/browser until the draft is cleared or submitted

## 8. Non-functional requirements

- mobile-first layout
- recoverable data entry flow via browser-local autosave on the same device/browser
- online-first writes for visit data and attachment uploads
- secure attachment handling
- explicit rollout and rollback notes
- staging smoke coverage for core visit flow

## 9. Acceptance criteria

- [ ] a project can contain multiple candidate properties
- [ ] each property can contain at least one visit record
- [ ] a visit cannot be marked complete until required checklist sections are filled
- [ ] uploaded photos remain linked to the correct visit
- [ ] an in-progress visit draft restores after refresh in the same browser on the same device before submission
- [ ] the report includes score, top notes, and red flags

## 10. Dependencies

- Next.js frontend shell
- FastAPI service
- PostgreSQL schema
- S3-compatible storage

## 11. Risks

- upload flow can become the hardest part of MVP
- checklist design can grow too broad
- browser-local autosave reduces note loss, but low-connectivity environments can still block server writes and attachment uploads

## 12. Release considerations

- no production auto deploy
- attachment storage path must be smoke tested
- autosave restore should be covered in smoke or manual regression before staging promotion
- rollback must be defined before staging promotion
