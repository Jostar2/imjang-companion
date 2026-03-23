from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "local"
    database_url: str = "sqlite:///./artifacts/imjang.db"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "imjang"
    postgres_user: str = "imjang"
    postgres_password: str = "imjang"
    s3_endpoint: str = "http://localhost:9000"
    s3_bucket: str = "imjang-uploads"
    s3_access_key: str = "minioadmin"
    s3_secret_key: str = "minioadmin"
    s3_region: str = "ap-northeast-2"
    storage_backend: str = "local"
    upload_root: str = "artifacts/uploads"
    web_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    admin_emails: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.web_origins.split(",") if origin.strip()]

    @property
    def allowed_admin_emails(self) -> set[str]:
        return {email.strip().lower() for email in self.admin_emails.split(",") if email.strip()}


settings = Settings()
repo_root = Path(__file__).resolve().parents[4]
