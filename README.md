# Imjang Companion

`Imjang Companion` is a standalone product repository managed by `Codex Launch OS`.

Its job is to prove one bounded product can move from brief through launch-readiness while keeping explicit business, QA, and release artifacts.

## Product thesis

- product thesis: a buyer-side due diligence workspace for structured field visits, comparison, and reporting
- business thesis: repeated-use operators such as buyer agents and small investor teams are the likely paying customer before individual buyers

## Project docs

- [project.json](./project.json)
- [docs/PLAN.md](./docs/PLAN.md)
- [docs/OPEN_QUESTIONS.md](./docs/OPEN_QUESTIONS.md)
- [docs/BUSINESS_MODEL.md](./docs/BUSINESS_MODEL.md)
- [docs/ICP.md](./docs/ICP.md)
- [docs/PRICING.md](./docs/PRICING.md)
- [docs/GTM.md](./docs/GTM.md)
- [docs/LAUNCH_RUNBOOK.md](./docs/LAUNCH_RUNBOOK.md)
- [docs/RELEASE_CHECKLIST.md](./docs/RELEASE_CHECKLIST.md)
- [docs/PRD.md](./docs/PRD.md)
- [docs/ADR/ADR-001.md](./docs/ADR/ADR-001.md)
- [briefs/real-estate-imjang-brief.md](./briefs/real-estate-imjang-brief.md)
- [runs/run-001-real-estate-imjang](./runs/run-001-real-estate-imjang)

## Repo layout

- web: `apps/web`
- api: `services/api`
- infra: `infra`
- docs: `docs`
- briefs: `briefs`
- runs: `runs`

## Current status

- run status: `execution_ready`
- current phase: `launch_os_execution`
- completed slices: project/property CRUD, visit workflow, comparison/report payloads, binary attachment uploads, upload failure recovery UX, admin ops console, role-based authorization, staging deploy bundle, deploy command contracts, v1 offline boundary decision
- next tasks: `staging_secret_population`

## Local commands

- `npm run api:dev`
- `npm run web:dev`
- `npm run web:lint`
- `npm run web:build`
- `npm run api:test`
- `npm run api:check`
- `npm run db:migrate`
- `npm run staging:preflight`
- `npm run release:check`
- `npm run release:governance`

## Open items

- validate whether staging or pilot evidence justifies expanding beyond browser-local autosave after v1
- populate GitHub environment secrets for staging and production command execution
- validate the first paying ICP through interviews or paid pilots
- complete launch artifacts for landing copy, onboarding, analytics, support, and pilot outreach

## Launch OS integration

`Codex Launch OS` manages this repository as an external project checkout.
The product repo stays responsible for product code, product docs, tests, infra, and release scripts.
