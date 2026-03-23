# Release Notes Draft

## Summary

Implemented the first bounded backend and frontend slices for the Imjang Companion MVP:

- project and property CRUD on the backend
- visit session and checklist completion rules on the backend
- local binary attachment upload for visits
- storage abstraction for local and S3-compatible backends
- SQLAlchemy-based persistent DB layer replaces the in-memory store
- user/session auth model now scopes data by owner
- buyer/admin role-based authorization now applies consistently across owner-scoped resources
- frontend routes now read and write through the backend API
- visit checklist now restores a browser-local autosave draft
- mobile-first project, property, and visit checklist shells on the frontend
- comparison and report now use dedicated backend payload contracts
- local end-to-end API smoke succeeded
- docker compose configuration parses successfully
- compose-based smoke succeeded with S3-compatible attachment upload
- staging deploy bundle and production approval workflow are in place
- environment-specific deploy commands now have a validated contract for staging and production
- visit completion now preserves the saved visit and offers retry UX for failed attachment uploads

## Verification

- `npm run api:test`
- `npm run api:check`
- `npm run web:lint`
- `npm run web:build`

## Deferred

- offline sync beyond browser-local autosave
- staged migration rollout policy
