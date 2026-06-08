from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from passlib.context import CryptContext
from app.db.base import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.schemas.auth import UserResponse
from app.schemas.user import (
    UpdateProfileRequest,
    ChangePasswordRequest,
    SubscriptionResponse,
    APIKeyResponse,
    CreateAPIKeyRequest,
    CreateAPIKeyResponse,
    NotificationResponse,
)

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_profile(
    request: UpdateProfileRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    update_data = request.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)
    await db.commit()
    await db.refresh(current_user)
    return current_user


@router.post("/me/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    request: ChangePasswordRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    if not pwd_context.verify(request.current_password, current_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")
    current_user.hashed_password = pwd_context.hash(request.new_password)
    await db.commit()


@router.get("/me/subscription", response_model=SubscriptionResponse)
async def get_subscription(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    from app.models.subscription import Subscription

    result = await db.execute(
        select(Subscription).where(Subscription.user_id == current_user.id)
    )
    subscription = result.scalar_one_or_none()
    if not subscription:
        return SubscriptionResponse(
            tier="free",
            status="active",
            price_usd=0.0,
            max_projects=3,
            max_agents_per_project=1,
            has_rag_access=False,
            has_pdf_export=False,
            has_ppt_export=False,
            has_api_access=False,
        )
    return subscription


@router.get("/me/api-keys", response_model=list[APIKeyResponse])
async def list_api_keys(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    from app.models.api_key import APIKey

    result = await db.execute(
        select(APIKey)
        .where(APIKey.user_id == current_user.id)
        .order_by(desc(APIKey.created_at))
    )
    return result.scalars().all()


@router.post("/me/api-keys", response_model=CreateAPIKeyResponse, status_code=status.HTTP_201_CREATED)
async def create_api_key(
    request: CreateAPIKeyRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    import secrets
    import hashlib

    from app.models.api_key import APIKey

    raw_key = f"ao_{secrets.token_urlsafe(32)}"
    key_prefix = raw_key[:10]
    last_five = raw_key[-5:]
    key_hash = hashlib.sha256(raw_key.encode()).hexdigest()

    api_key = APIKey(
        user_id=current_user.id,
        name=request.name,
        key_hash=key_hash,
        key_prefix=key_prefix,
        last_five=last_five,
    )
    db.add(api_key)
    await db.commit()
    await db.refresh(api_key)

    return CreateAPIKeyResponse(
        api_key=raw_key,
        key_data=APIKeyResponse.model_validate(api_key),
    )


@router.get("/me/notifications", response_model=list[NotificationResponse])
async def list_notifications(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    from app.models.notification import Notification

    result = await db.execute(
        select(Notification)
        .where(Notification.user_id == current_user.id)
        .order_by(desc(Notification.created_at))
        .limit(50)
    )
    return result.scalars().all()
