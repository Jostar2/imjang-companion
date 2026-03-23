from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    region: str | None = Field(default=None, max_length=120)
    budget: str | None = Field(default=None, max_length=120)
    notes: str | None = Field(default=None, max_length=1000)


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    region: str | None = Field(default=None, max_length=120)
    budget: str | None = Field(default=None, max_length=120)
    notes: str | None = Field(default=None, max_length=1000)


class ProjectResponse(BaseModel):
    id: str
    owner_user_id: str | None = None
    name: str
    region: str | None = None
    budget: str | None = None
    notes: str | None = None
