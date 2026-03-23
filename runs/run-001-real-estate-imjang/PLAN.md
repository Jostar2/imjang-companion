# PLAN.md

## Project
- Name: Imjang Companion MVP
- Owner: Codex local manager
- Stack: Next.js + FastAPI + PostgreSQL + S3 + AWS ECS
- Repo: C:\Users\josta\Downloads\codex-launch-os
- Run ID: run-001-real-estate-imjang
- Operating mode: `local-bootstrap`

## Goal
- 이번 실행의 목표: planning package를 만들고 bounded implementation task를 정의한다
- 성공 기준: PRD, scope, acceptance, architecture, risk, task graph, task packet 2개 이상 생성
- 배포 대상: staging readiness only

## Scope
### In
- visit project 생성
- property 등록
- visit checklist
- notes/scores/photos
- comparison view
- summary report

### Out
- live brokerage integration
- payment
- legal due diligence
- realtime collaboration
- production release

## Constraints
- mobile-first UX
- staging required
- prod manual approval
- no heavy external listing integrations in v1

## Acceptance criteria
- [ ] user can create a visit project
- [ ] user can register candidate properties
- [ ] user can complete a visit checklist with notes, scores, and photos
- [ ] comparison view shows score and red flags
- [ ] summary report can be generated for a visited property

## Open questions
- blocker: offline draft-save required or nice-to-have?
- non-blocker: partner sharing as view-only in v1 or later?

## Task graph
1. planner outputs
2. architect outputs
3. BE-001 project/property CRUD
4. BE-002 visit checklist and scoring
5. FE-001 mobile project/property screens
6. FE-002 visit checklist flow
7. QA-001 regression and smoke plan
8. INF-001 upload and staging readiness

## Parallel lanes
- Lane A: backend CRUD and visit domain
- Lane B: mobile UI and comparison/report
- Lane C: QA and staging readiness

## Task packet summary
- packet exists: yes
- read_files: current run artifacts plus repo-local implementation files
- write_scope: bounded by task packet and real repo paths
- acceptance subset: yes
- verification commands: `npm run web:lint`, `npm run web:build`, `npm run api:test`, `npm run api:check`

## Model routing
- manager/planner/architect/reviewer: `gpt-5.4`
- coding fast lane: `gpt-5.3-codex-spark`
- lightweight triage: `gpt-5.4-mini`
- scripted CI fallback: `gpt-5.3-codex`

## Escalation ladder
- default coding: `gpt-5.3-codex-spark`
- retry or context overflow: `gpt-5.3-codex`
- design or release risk: `gpt-5.4`

## Risks
- attachment upload complexity can slow MVP
- mobile UX can sprawl without a tight checklist contract
- offline expectation may expand scope

## Verification
- lint: `npm run web:lint`
- tests: `npm run api:test`
- build: `npm run web:build`
- smoke: create project, add property, complete visit, view report

## Release notes draft
- initial planning package for real-estate field visit MVP

## Rollback draft
- trigger: staging smoke failure or upload path failure
- procedure: block release candidate and revert feature branch
- owner: reviewer + infra owner
