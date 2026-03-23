from services.api.app.core.db import reset_db


def reset_store() -> None:
    reset_db()
