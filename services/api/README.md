# API Service

FastAPI service for the Imjang Companion MVP.

Current status:

- auth, project, property, visit, report, and ops routes are implemented
- buyer/admin role-based access control is active for owner-scoped resources
- attachment uploads support inline/local storage and S3-compatible backends
- pytest coverage exists for health, CRUD placeholders, visit flows, and authz checks

Suggested local setup:

1. `python -m venv .venv`
2. `.venv\\Scripts\\activate`
3. `pip install -r services/api/requirements.txt`
4. `alembic upgrade head`
5. `uvicorn services.api.app.main:app --reload`
6. `python -m pytest services/api/tests -q`
