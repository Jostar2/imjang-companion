from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
STAGING_DIR = ROOT / "infra" / "staging"

REQUIRED_FILES = [
    STAGING_DIR / ".env.staging.example",
    STAGING_DIR / "DEPLOYMENT.md",
    STAGING_DIR / "docker-compose.staging.yml",
    ROOT / ".github" / "workflows" / "deploy-staging.yml",
]

REQUIRED_ENV_KEYS = [
    "API_IMAGE",
    "WEB_IMAGE",
    "DATABASE_URL",
    "S3_BUCKET",
    "S3_ACCESS_KEY",
    "S3_SECRET_KEY",
    "WEB_ORIGINS",
    "NEXT_PUBLIC_API_BASE_URL",
    "ADMIN_EMAILS",
]


def main() -> int:
    missing_files = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.exists()]
    if missing_files:
        print("Missing staging files:")
        for path in missing_files:
            print(f"- {path}")
        return 1

    env_example = (STAGING_DIR / ".env.staging.example").read_text(encoding="utf8")
    missing_keys = [key for key in REQUIRED_ENV_KEYS if f"{key}=" not in env_example]
    if missing_keys:
        print("Missing required keys in .env.staging.example:")
        for key in missing_keys:
            print(f"- {key}")
        return 1

    print("staging-preflight-ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
