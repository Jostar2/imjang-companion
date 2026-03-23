# Production Deploy Contract

Production deployment remains operator-approved and environment-specific. The workflow validates that the command secrets satisfy this contract before human approval can proceed.

## Required production secrets

- `PRODUCTION_REMOTE_PATH`
- `PRODUCTION_DEPLOY_COMMAND`
- `PRODUCTION_ROLLBACK_COMMAND`

## Command contract

- `PRODUCTION_REMOTE_PATH` must point to a dedicated deploy directory, not `/`, `~`, or `.`
- commands are executed after `cd $PRODUCTION_REMOTE_PATH`
- each command must be stored as a single-line secret
- deploy and rollback commands must be different
- avoid destructive global cleanup commands such as `rm -rf /`, `git reset --hard`, or `docker system prune`
- if production uses Docker Compose, the remote host should already contain the production compose and env files referenced by the commands

## Example commands

Remote path:

```text
~/imjang-production/app
```

Deploy command:

```text
docker compose --env-file .env.production -f docker-compose.production.yml pull && docker compose --env-file .env.production -f docker-compose.production.yml up -d
```

Rollback command:

```text
docker compose --env-file .env.production -f docker-compose.production.yml down && docker compose --env-file .env.production -f docker-compose.production.yml up -d
```

The production compose and env files are expected to be provisioned on the remote host and are not versioned in this template repository.
