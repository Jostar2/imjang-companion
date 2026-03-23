# Staging Deploy Contract

This staging bundle is designed to be copied to a remote host and deployed by environment-specific commands supplied through GitHub Actions secrets.

## Required staging secrets

- `STAGING_SSH_HOST`
- `STAGING_SSH_USER`
- `STAGING_SSH_KEY`
- `STAGING_DATABASE_URL`
- `STAGING_POSTGRES_DB`
- `STAGING_POSTGRES_USER`
- `STAGING_POSTGRES_PASSWORD`
- `STAGING_S3_ENDPOINT`
- `STAGING_S3_BUCKET`
- `STAGING_S3_ACCESS_KEY`
- `STAGING_S3_SECRET_KEY`
- `STAGING_S3_REGION`
- `STAGING_WEB_ORIGINS`
- `STAGING_PUBLIC_API_BASE_URL`
- `STAGING_ADMIN_EMAILS`
- `STAGING_REMOTE_PATH`
- `STAGING_DEPLOY_COMMAND`
- `STAGING_ROLLBACK_COMMAND`

## Example commands

Remote path:

```text
~/imjang-staging/infra/staging
```

Deploy command:

```text
docker compose --env-file .env.staging -f docker-compose.staging.yml pull && docker compose --env-file .env.staging -f docker-compose.staging.yml up -d
```

Rollback command:

```text
docker compose --env-file .env.staging -f docker-compose.staging.yml down && docker compose --env-file .env.staging -f docker-compose.staging.yml up -d
```

## Command contract

- `STAGING_REMOTE_PATH` must point to a dedicated deploy directory, not `/`, `~`, or `.`
- `STAGING_DEPLOY_COMMAND` and `STAGING_ROLLBACK_COMMAND` are executed after `cd $STAGING_REMOTE_PATH`
- each command must be stored as a single-line secret
- both commands must reference `.env.staging` and `docker-compose.staging.yml`
- deploy and rollback commands must be different
- avoid destructive global cleanup commands such as `rm -rf /`, `git reset --hard`, or `docker system prune`

Production deployment remains manual, but the same command contract is expected through `PRODUCTION_REMOTE_PATH`, `PRODUCTION_DEPLOY_COMMAND`, and `PRODUCTION_ROLLBACK_COMMAND`.
