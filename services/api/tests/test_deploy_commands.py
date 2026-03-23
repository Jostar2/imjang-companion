from scripts.check_deploy_commands import validate_environment_contract


def test_staging_contract_accepts_compose_based_commands() -> None:
    errors = validate_environment_contract(
        "staging",
        {
            "STAGING_REMOTE_PATH": "~/imjang-staging/infra/staging",
            "STAGING_DEPLOY_COMMAND": "docker compose --env-file .env.staging -f docker-compose.staging.yml pull && docker compose --env-file .env.staging -f docker-compose.staging.yml up -d",
            "STAGING_ROLLBACK_COMMAND": "docker compose --env-file .env.staging -f docker-compose.staging.yml down && docker compose --env-file .env.staging -f docker-compose.staging.yml up -d",
        },
    )

    assert errors == []


def test_staging_contract_requires_staging_bundle_references() -> None:
    errors = validate_environment_contract(
        "staging",
        {
            "STAGING_REMOTE_PATH": "~/imjang-staging/infra/staging",
            "STAGING_DEPLOY_COMMAND": "docker compose up -d",
            "STAGING_ROLLBACK_COMMAND": "docker compose down && docker compose up -d",
        },
    )

    assert "STAGING_DEPLOY_COMMAND must reference `.env.staging`" in errors
    assert "STAGING_DEPLOY_COMMAND must reference `docker-compose.staging.yml`" in errors


def test_contract_rejects_identical_deploy_and_rollback_commands() -> None:
    errors = validate_environment_contract(
        "production",
        {
            "PRODUCTION_REMOTE_PATH": "~/imjang-production/app",
            "PRODUCTION_DEPLOY_COMMAND": "./deploy-prod.sh",
            "PRODUCTION_ROLLBACK_COMMAND": "./deploy-prod.sh",
        },
    )

    assert "PRODUCTION_DEPLOY_COMMAND and PRODUCTION_ROLLBACK_COMMAND must be different" in errors


def test_contract_rejects_dangerous_commands() -> None:
    errors = validate_environment_contract(
        "production",
        {
            "PRODUCTION_REMOTE_PATH": "~/imjang-production/app",
            "PRODUCTION_DEPLOY_COMMAND": "docker system prune -af && ./deploy-prod.sh",
            "PRODUCTION_ROLLBACK_COMMAND": "./rollback-prod.sh",
        },
    )

    assert "PRODUCTION_DEPLOY_COMMAND contains a forbidden pattern: docker system prune" in errors


def test_contract_rejects_broad_remote_paths() -> None:
    errors = validate_environment_contract(
        "staging",
        {
            "STAGING_REMOTE_PATH": "/",
            "STAGING_DEPLOY_COMMAND": "docker compose --env-file .env.staging -f docker-compose.staging.yml up -d",
            "STAGING_ROLLBACK_COMMAND": "docker compose --env-file .env.staging -f docker-compose.staging.yml down && docker compose --env-file .env.staging -f docker-compose.staging.yml up -d",
        },
    )

    assert "STAGING_REMOTE_PATH is too broad; use a dedicated deploy directory" in errors
