from dataclasses import dataclass


@dataclass(slots=True)
class Attachment:
    id: str
    visit_id: str
    filename: str
    content_type: str
    category: str
    storage_backend: str
    storage_key: str
    size_bytes: int
