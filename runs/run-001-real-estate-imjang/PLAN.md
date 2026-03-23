# PLAN.md

## Project
- Name: Imjang Companion MVP
- Owner: Codex local manager
- Stack: Next.js + FastAPI + PostgreSQL + S3 + AWS ECS
- Repo: C:\Users\josta\Downloads\imjang-companion
- Run ID: run-001-real-estate-imjang
- Operating mode: `standalone-product-repo`

## Goal
- 이번 실행의 목표: 현재 구현 상태를 기준으로 v1 범위를 고정하고, 로컬 데모/파일럿 운영 기준과 첫 paid pilot 준비 문서를 launch-ready 수준으로 정리한다
- 성공 기준: offline boundary, autosave behavior, local walkthrough, launch artifacts, and pilot assumptions가 현재 구현과 일치한다
- 배포 대상: local-first walkthrough and pilot prep

## Scope
### In
- authenticated project/property CRUD
- visit capture with required checklist sections
- browser-local autosave and same-browser draft restore
- attachment upload and failed-upload retry UX
- comparison and report read views
- release, smoke, and pilot-launch artifacts

### Out
- live brokerage integration
- payment
- legal due diligence
- realtime collaboration
- production release
- partial offline queueing 또는 sync
- offline attachment upload
- cross-device draft restore

## Constraints
- mobile-first UX
- remote staging은 선택사항으로 미루고, 당장은 local walkthrough와 pilot feedback을 우선한다
- prod manual approval
- no heavy external listing integrations in v1
- visit writes와 attachment upload는 v1에서 online-first로 유지
- single-user owner scope를 넘는 collaboration은 v1 범위 밖

## Acceptance criteria
- [ ] product docs와 run docs가 current implementation과 같은 방향을 가리킨다
- [ ] autosave restore와 attachment retry가 smoke와 launch docs에 반영된다
- [ ] launch artifact 파일이 존재하고 pilot 준비에 바로 쓸 수 있다
- [ ] next tasks가 실제 남은 human gates와 business validation으로 압축된다

## Open questions
- blocker: none currently. `offline_support_decision` is closed for v1 as `online-first + browser-local autosave/restore`.
- non-blocker: partner sharing as view-only in v1 or later?

## Locked decisions for this run
- first paying ICP: `independent buyer agent`
- first working offer: `2-week founder-led paid pilot`
- internal working ask: `KRW 149,000`
- seeded outreach list: `5 founder-owned lead slots prepared on 2026-03-23`

## Task graph
1. rehearse a local demo path for project -> property -> visit -> comparison -> report
2. refresh local smoke coverage for autosave restore and attachment retry
3. finalize launch artifacts for landing, onboarding, analytics, support, and pilots
4. run founder-owned outreach against the 5 seeded lead slots
5. defer staging setup until local walkthroughs produce real pilot demand

## Parallel lanes
- Lane A: product reliability and smoke coverage
- Lane B: launch asset completion and onboarding clarity
- Lane C: ICP, offer, and pilot validation

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
- browser-local autosave reduces session loss, but low-connectivity environments can still block API writes and attachment uploads
- payer ambiguity can slow launch if report quality is not compelling enough for buyer agents or investor teams
- launch assets can lag behind working code and create a false sense of readiness

## Verification
- lint: `npm run web:lint`
- tests: `npm run api:test`
- build: `npm run web:build`
- smoke: create project, add property, complete visit, refresh draft restore, retry failed attachment upload, view report

## Release notes draft
- initial planning package for real-estate field visit MVP

## Rollback draft
- trigger: local walkthrough failure or upload path failure
- procedure: block the pilot-facing demo path, keep the capture flow protected, and defer hosted deployment work
- owner: reviewer + infra owner
