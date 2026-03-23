from pydantic import BaseModel, Field


class AttachmentCreate(BaseModel):
    filename: str = Field(min_length=1, max_length=200)
    content_type: str = Field(min_length=1, max_length=120)
    category: str = Field(min_length=1, max_length=80)


class AttachmentResponse(BaseModel):
    id: str
    visit_id: str
    filename: str
    content_type: str
    category: str
    storage_backend: str
    storage_key: str
    size_bytes: int
