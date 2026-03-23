# PLAN.md

## Project
- Name: Imjang Companion MVP
- Owner: Codex local manager
- Stack: Next.js + FastAPI + PostgreSQL + S3-compatible object storage + AWS ECS
- Repo: C:\Users\josta\Downloads\codex-launch-os
- Run ID: run-001-real-estate-imjang
- Operating mode: `local-bootstrap`

## Goal
- 이번 실행의 목표: planning package를 기준으로 bounded implementation repo를 준비하고 첫 coding slice를 시작할 수 있게 만든다
- 성공 기준: repo 구조, active plan, task graph, task packets, verification commands가 실제 경로 기준으로 정리된다
- 배포 대상: staging readiness only

## Product + launch thesis
- product thesis: 임장 현장의 관찰과 판단을 구조화해서 비교와 보고서로 복원 가능한 buyer-side due diligence workflow를 만든다
- platform thesis: Codex가 planning, architecture, implementation, QA, release, GTM artifacts까지 통제하는 launch operating system으로 확장한다

## Scope
### In
- project/property CRUD skeleton
- visit workflow shell
- comparison/report shell
- backend API skeleton
- local infra skeleton
- active planning artifacts

### Out
- production deploy
- real listing integration
- OCR
- realtime collaboration

## Constraints
- mobile-first frontend
- local bootstrap first
- staging required before any prod discussion
- Spark only with task packets

## Acceptance criteria
- [ ] active run package exists in repo
- [ ] `BE-001` and `FE-001` packets point to real repo paths
- [ ] frontend and backend skeletons exist for the first bounded tasks
- [ ] verification commands are explicit and repo-local

## Open questions
- blocker: do we need autosave-only or partial offline support in MVP?
- non-blocker: should report export remain web-only in v1?

## Task graph
1. planning artifacts
2. architecture artifacts
3. BE-001 project/property CRUD
4. FE-001 project/property screens
5. BE-002 visit checklist domain
6. FE-002 visit checklist flow
7. QA-001 regression and smoke plan
8. INF-001 staging readiness

## Parallel lanes
- Lane A: backend core CRUD
- Lane B: mobile project/property UI
- Lane C: QA and release preparation

## Task packet summary
- packet exists: yes
- read_files: real repo files plus current run artifacts
- write_scope: bounded by task packet
- acceptance subset: yes
- verification commands: repo-local

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
- attachment flow may expand scope quickly
- visit checklist taxonomy may drift without discipline
- frontend shells may look complete before domain contracts are real

## Verification
- lint: `npm run web:lint`
- tests: `npm run api:test`
- build: `npm run web:build`
- smoke: create project, add property, complete visit, view report

## Release notes draft
- initialized target repo and aligned planning artifacts with real implementation paths

## Rollback draft
- trigger: repo skeleton blocks bounded task execution or local verification fails
- procedure: revert to planning package only and regenerate task packet boundaries
- owner: reviewer + infra owner
