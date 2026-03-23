# AGENTS.md

## Repository expectations

- Read `project.json` first.
- Read the local product docs before changing code:
  - `README.md`
  - `docs/PLAN.md`
  - `docs/OPEN_QUESTIONS.md`
  - `docs/RELEASE_CHECKLIST.md`
- If the task touches monetization, launch, onboarding, or pricing, also read:
  - `docs/BUSINESS_MODEL.md`
  - `docs/ICP.md`
  - `docs/PRICING.md`
  - `docs/GTM.md`
  - `docs/LAUNCH_RUNBOOK.md`
- Read the active run package under `runs/run-001-real-estate-imjang/`.

## Working agreement

- Keep changes bounded to the product repo.
- Treat auth, permission, pricing, release policy, and infra changes as high risk.
- Update docs when API contracts, release steps, pricing assumptions, or repeated reviewer feedback change.

## Verification commands

- `npm run web:lint`
- `npm run web:build`
- `npm run api:test`
- `npm run api:check`
- `npm run release:check`
- `npm run release:governance`
