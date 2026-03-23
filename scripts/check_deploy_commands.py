from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Mapping


ENV_MAP = {
    "staging": {
        "required_keys": ["STAGING_REMOTE_PATH", "STAGING_DEPLOY_COMMAND", "STAGING_ROLLBACK_COMMAND"],
        "required_substrings": {
            "STAGING_DEPLOY_COMMAND": ["docker compose", ".env.staging", "docker-compose.staging.yml"],
            "STAGING_ROLLBACK_COMMAND": ["docker compose", ".env.staging", "docker-compose.staging.yml"],
        },
    },
    "production": {
        "required_keys": ["PRODUCTION_REMOTE_PATH", "PRODUCTION_DEPLOY_COMMAND", "PRODUCTION_ROLLBACK_COMMAND"],
        "required_substrings": {},
    },
}

DANGEROUS_PATTERNS = [
    "rm -rf /",
    "rm -fr /",
    "git reset --hard",
    "git checkout --",
    "docker system prune",
    "docker volume prune",
    "kubectl delete namespace",
    "mkfs",
    "shutdown",
    "reboot",
]


def normalize_command(value: str) -> str:
    return " ".join(value.split())


def validate_remote_path(key: str, value: str) -> list[str]:
    errors: list[str] = []
    normalized = value.strip()
    if not normalized:
        return [f"{key} is missing"]
    if "\n" in normalized or "\r" in normalized:
        errors.append(f"{key} must be a single-line path")
    if any(char.isspace() for char in normalized):
        errors.append(f"{key} must not contain whitespace")
    if normalized in {"/", ".", "~"}:
        errors.append(f"{key} is too broad; use a dedicated deploy directory")
    return errors


def validate_command_value(key: str, value: str) -> list[str]:
    errors: list[str] = []
    normalized = value.strip()
    if not normalized:
        return [f"{key} is missing"]
    if "\n" in normalized or "\r" in normalized:
        errors.append(f"{key} must be a single-line command")

    lowered = normalize_command(normalized).lower()
    for pattern in DANGEROUS_PATTERNS:
        if pattern in lowered:
            errors.append(f"{key} contains a forbidden pattern: {pattern}")
    return errors


def validate_environment_contract(environment: str, values: Mapping[str, str]) -> list[str]:
    contract = ENV_MAP[environment]
    errors: list[str] = []
    resolved = {key: values.get(key, "").strip() for key in contract["required_keys"]}

    missing = [key for key, value in resolved.items() if not value]
    if missing:
        for key in missing:
            errors.append(f"Missing required variable: {key}")
        return errors

    remote_path_key, deploy_key, rollback_key = contract["required_keys"]
    errors.extend(validate_remote_path(remote_path_key, resolved[remote_path_key]))
    errors.extend(validate_command_value(deploy_key, resolved[deploy_key]))
    errors.extend(validate_command_value(rollback_key, resolved[rollback_key]))

    if normalize_command(resolved[deploy_key]).lower() == normalize_command(resolved[rollback_key]).lower():
        errors.append(f"{deploy_key} and {rollback_key} must be different")

    for key, expected_substrings in contract["required_substrings"].items():
        command = resolved[key]
        for expected in expected_substrings:
            if expected not in command:
                errors.append(f"{key} must reference `{expected}`")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify that environment-specific deploy command secrets satisfy the contract.")
    parser.add_argument("--environment", choices=sorted(ENV_MAP.keys()), required=True)
    args = parser.parse_args()

    errors = validate_environment_contract(args.environment, os.environ)
    if errors:
        print(f"{args.environment}-deploy-command-contract-failed")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"{args.environment}-deploy-commands-ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
