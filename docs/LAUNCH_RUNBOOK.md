# LAUNCH_RUNBOOK.md

## Launch objective

A launch is not complete when code passes tests. A launch is complete when:

- a clear paying customer exists
- the pricing offer is explicit
- onboarding, activation, and report delivery are measurable
- a real user can reach value in staging or production-like conditions

## Launch phases

### 1. Thesis lock

Owner:

- `planner`
- `business_strategist`

Outputs:

- `PRD.md`
- `BUSINESS_MODEL.md`
- `ICP.md`
- `PRICING.md`
- `GTM.md`

### 2. Product build

Owner:

- `architect`
- bounded coding workers
- `qa_worker`

Outputs:

- ADR
- task graph
- task packets
- working product slices
- verification evidence

### 3. Launch readiness

Owner:

- `launch_operator`
- `infra_release`

Outputs:

- deploy command contracts
- release checklist
- smoke plan
- analytics event map
- billing and onboarding backlog

### 4. Paid pilot

Owner:

- `launch_operator`
- human founder

Outputs:

- pilot offer
- pilot customer list
- conversion notes
- objections and pricing feedback

### 5. General release

Owner:

- human approval gate
- `launch_operator`

Outputs:

- launch announcement
- onboarding path
- support runbook
- KPI review cadence

## Agent ownership

- `planner`: product problem, scope, open questions
- `business_strategist`: ICP, monetization, pricing, offer design
- `architect`: architecture, slices, risk, rollback
- `backend_worker` / `frontend_worker`: implementation
- `qa_worker`: regression and smoke validation
- `infra_release`: CI, staging, deploy safety
- `launch_operator`: GTM, launch checklist, KPI instrumentation, rollout sequencing

## Automated gates

- docs are present and current
- task scope is explicit
- build and test gates pass
- staging smoke passes
- launch docs exist for ICP, pricing, GTM, and runbook

## Human gates

- production approval
- secret population
- payment policy
- legal or compliance claims
- pricing go-live

## Minimum launch artifacts

- landing page copy
- offer page or pricing sheet
- onboarding path
- activation event definitions
- support and rollback notes
- paid pilot contact list

## KPI review cadence

- daily during pilot week
- weekly after the first paid accounts

## Stop conditions

Stop the automation loop and request human input if:

- there is no clear payer
- there is no plausible acquisition channel
- pricing cannot be defended
- launch requires new legal, payment, or secret decisions
