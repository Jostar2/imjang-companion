# PLAN.md

## Project
- Name: Imjang Companion MVP
- Owner: Codex local manager
- Stack: Next.js + FastAPI + PostgreSQL + S3-compatible object storage + AWS ECS
- Repo: C:\Users\josta\Downloads\imjang-companion
- Run ID: run-001-real-estate-imjang
- Operating mode: `standalone-product-repo`

## Goal
- 이번 실행의 목표: 현재 구현 상태를 기준으로 v1 범위를 고정하고, 로컬 데모/파일럿 운영 기준과 첫 paid pilot 준비 문서를 launch-ready 수준으로 정리한다
- 성공 기준: offline boundary, autosave behavior, local walkthrough, launch artifacts, and pilot assumptions가 현재 구현과 일치한다
- 배포 대상: local-first walkthrough and pilot prep

## Product + launch thesis
- product thesis: 임장 현장의 관찰과 판단을 구조화해서 비교와 보고서로 복원 가능한 buyer-side due diligence workflow를 만든다
- platform thesis: Codex가 planning, architecture, implementation, QA, release, GTM artifacts까지 통제하는 launch operating system으로 확장한다

## Scope
### In
- authenticated project/property CRUD
- visit capture with required checklist sections
- browser-local autosave and same-browser draft restore
- attachment upload and failed-upload retry UX
- comparison and report read views
- release, smoke, and pilot-launch artifacts

### Out
- production deploy
- real listing integration
- OCR
- realtime collaboration
- partial offline mutation queueing
- offline attachment upload
- cross-device draft restore

## Constraints
- mobile-first frontend
- local bootstrap first
- remote staging은 선택사항으로 미루고, 당장은 local walkthrough와 pilot feedback을 우선한다
- Spark only with task packets
- visit writes and attachment uploads remain online-first in v1
- single-user owner scope remains the product boundary in v1

## Acceptance criteria
- [ ] product docs reflect the current implementation surface and repo boundary
- [ ] autosave restore and attachment retry are explicit in PRD, acceptance, and release docs
- [ ] smoke criteria cover project creation, property creation, visit completion, draft restore, and comparison/report
- [ ] launch artifacts exist for landing copy, onboarding, analytics, support, and paid pilot outreach

## Open questions
- blocker: none currently. `offline_support_decision` is closed for v1 as `online-first + browser-local autosave/restore`.
- non-blocker: should report export remain web-only in v1?

## Task graph
1. rehearse a local demo path for project -> property -> visit -> comparison -> report
2. refresh local smoke coverage for autosave restore and attachment retry
3. finalize launch artifacts for landing, onboarding, analytics, support, and pilots
4. validate first payer and first paid offer through interviews or local pilots
5. defer staging setup until local walkthroughs produce real pilot demand

## Parallel lanes
- Lane A: product reliability and smoke coverage
- Lane B: launch asset completion and onboarding clarity
- Lane C: ICP, offer, and pilot validation

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
- low-connectivity environments can still block server writes and attachment uploads even though draft restore works
- payer ambiguity can slow launch if report quality is not compelling enough for buyer agents or investor teams
- launch assets can lag behind working code and create a false sense of readiness

## Verification
- lint: `npm run web:lint`
- tests: `npm run api:test`
- build: `npm run web:build`
- smoke: create project, add property, complete visit, refresh draft restore, retry failed attachment upload, view report

## Release notes draft
- aligned product docs to the standalone repo, explicit v1 online-first boundary, and launch-readiness artifacts

## Rollback draft
- trigger: local walkthrough reveals regression in capture, autosave restore, upload retry, or report clarity
- procedure: keep capture path as the protected lane, hide unstable read surfaces if necessary, and defer scope-expanding launch promises or hosted deployment work
- owner: reviewer + infra owner + launch operator
