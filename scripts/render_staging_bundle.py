from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


REQUIRED_ENV = {
    "API_IMAGE": "API_IMAGE",
    "WEB_IMAGE": "WEB_IMAGE",
    "DATABASE_URL": "STAGING_DATABASE_URL",
    "POSTGRES_DB": "STAGING_POSTGRES_DB",
    "POSTGRES_USER": "STAGING_POSTGRES_USER",
    "POSTGRES_PASSWORD": "STAGING_POSTGRES_PASSWORD",
    "S3_ENDPOINT": "STAGING_S3_ENDPOINT",
    "S3_BUCKET": "STAGING_S3_BUCKET",
    "S3_ACCESS_KEY": "STAGING_S3_ACCESS_KEY",
    "S3_SECRET_KEY": "STAGING_S3_SECRET_KEY",
    "S3_REGION": "STAGING_S3_REGION",
    "WEB_ORIGINS": "STAGING_WEB_ORIGINS",
    "NEXT_PUBLIC_API_BASE_URL": "STAGING_PUBLIC_API_BASE_URL",
    "ADMIN_EMAILS": "STAGING_ADMIN_EMAILS",
}

REQUIRED_COMMAND_ENV = [
    "STAGING_REMOTE_PATH",
    "STAGING_DEPLOY_COMMAND",
    "STAGING_ROLLBACK_COMMAND",
]


def read_required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Render staging env and deploy manifest from CI secrets.")
    parser.add_argument("--env-file", required=True, help="Path to the rendered .env.staging file.")
    parser.add_argument("--manifest", required=True, help="Path to the rendered deploy manifest json.")
    args = parser.parse_args()

    env_file = Path(args.env_file)
    manifest_file = Path(args.manifest)
    env_file.parent.mkdir(parents=True, exist_ok=True)
    manifest_file.parent.mkdir(parents=True, exist_ok=True)

    rendered_env: dict[str, str] = {
        "COMPOSE_PROJECT_NAME": "imjang-staging",
        "API_PORT": "8000",
        "WEB_PORT": "3000",
        "STORAGE_BACKEND": "s3",
    }
    for target_key, source_key in REQUIRED_ENV.items():
        rendered_env[target_key] = read_required_env(source_key)

    env_text = "\n".join(f"{key}={value}" for key, value in rendered_env.items()) + "\n"
    env_file.write_text(env_text, encoding="utf8")

    manifest = {
        "remote_path": read_required_env("STAGING_REMOTE_PATH"),
        "deploy_command": read_required_env("STAGING_DEPLOY_COMMAND"),
        "rollback_command": read_required_env("STAGING_ROLLBACK_COMMAND"),
        "api_base_url": rendered_env["NEXT_PUBLIC_API_BASE_URL"],
        "api_image": rendered_env["API_IMAGE"],
        "web_image": rendered_env["WEB_IMAGE"],
    }
    for key in REQUIRED_COMMAND_ENV:
        read_required_env(key)
    manifest_file.write_text(json.dumps(manifest, indent=2), encoding="utf8")

    print("staging-bundle-rendered")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"staging-bundle-render-failed: {error}", file=sys.stderr)
        raise
