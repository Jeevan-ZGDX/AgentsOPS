from typing import Optional
from pydantic import BaseModel, Field


class UpdateProfileRequest(BaseModel):
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8)


class SubscriptionResponse(BaseModel):
    tier: str
    status: str
    current_period_end: Optional[str] = None
    price_usd: float
    max_projects: int
    max_agents_per_project: int
    has_rag_access: bool
    has_pdf_export: bool
    has_ppt_export: bool
    has_api_access: bool

    model_config = {"from_attributes": True}


class APIKeyResponse(BaseModel):
    id: int
    name: str
    key_prefix: str
    last_five: str
    is_active: bool
    created_at: str
    last_used_at: Optional[str] = None

    model_config = {"from_attributes": True}


class CreateAPIKeyRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)


class CreateAPIKeyResponse(BaseModel):
    api_key: str
    key_data: APIKeyResponse


class NotificationResponse(BaseModel):
    id: int
    type: str
    priority: str
    title: str
    message: str
    is_read: bool
    created_at: str

    model_config = {"from_attributes": True}
