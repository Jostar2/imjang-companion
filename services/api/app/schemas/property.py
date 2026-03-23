from pydantic import BaseModel, Field


class PropertyCreate(BaseModel):
    project_id: str = Field(min_length=1)
    address: str = Field(min_length=1, max_length=240)
    listing_price: int | None = Field(default=None, ge=0)
    property_type: str | None = Field(default=None, max_length=80)
    source: str | None = Field(default=None, max_length=120)


class PropertyUpdate(BaseModel):
    address: str | None = Field(default=None, min_length=1, max_length=240)
    listing_price: int | None = Field(default=None, ge=0)
    property_type: str | None = Field(default=None, max_length=80)
    source: str | None = Field(default=None, max_length=120)


class PropertyResponse(BaseModel):
    id: str
    project_id: str
    owner_user_id: str | None = None
    address: str
    listing_price: int | None = None
    property_type: str | None = None
    source: str | None = None
