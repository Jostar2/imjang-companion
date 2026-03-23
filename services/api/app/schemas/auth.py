from pydantic import BaseModel, EmailStr, Field
from typing import Literal


class LoginRequest(BaseModel):
    email: EmailStr
    display_name: str = Field(min_length=1, max_length=120)
    role: Literal["buyer", "admin"] = "buyer"


class SessionResponse(BaseModel):
    token: str
    user_id: str
    email: EmailStr
    display_name: str
    role: Literal["buyer", "admin"]


class MeResponse(BaseModel):
    user_id: str
    email: EmailStr
    display_name: str
    role: Literal["buyer", "admin"]
