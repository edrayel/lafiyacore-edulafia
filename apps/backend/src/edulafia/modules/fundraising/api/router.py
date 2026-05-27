"""Fundraising API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.database import get_db
from edulafia.dependencies import CurrentUser
from edulafia.modules.fundraising.repository import CampaignRepository, DonationRepository
from edulafia.modules.fundraising.schemas import (
    CampaignCreate,
    CampaignResponse,
    CampaignUpdate,
    DonationCreate,
    DonationResponse,
)
from edulafia.modules.fundraising.service import CampaignService, DonationService

router = APIRouter(prefix="/fundraising", tags=["Fundraising"])


def get_campaign_service(db: AsyncSession = Depends(get_db)) -> CampaignService:
    """Dependency to get CampaignService."""
    repository = CampaignRepository(db)
    return CampaignService(repository)


def get_donation_service(db: AsyncSession = Depends(get_db)) -> DonationService:
    """Dependency to get DonationService."""
    repository = DonationRepository(db)
    return DonationService(repository)


@router.post(
    "/campaigns",
    response_model=CampaignResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a campaign",
)
async def create_campaign(
    data: CampaignCreate,
    current_user: CurrentUser,
    service: CampaignService = Depends(get_campaign_service),
) -> CampaignResponse:
    """Create a new fundraising campaign."""
    try:
        return await service.create(
            data=data,
            user_id=UUID(current_user["sub"]),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/campaigns/{campaign_id}",
    response_model=CampaignResponse,
    summary="Get a campaign by ID",
)
async def get_campaign(
    campaign_id: UUID,
    current_user: CurrentUser,
    service: CampaignService = Depends(get_campaign_service),
) -> CampaignResponse:
    """Get a campaign by ID."""
    campaign = await service.get_by_id(
        campaign_id=campaign_id,
        school_id=UUID(current_user["school_id"]),
    )
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found",
        )
    return campaign


@router.get(
    "/campaigns",
    response_model=list[CampaignResponse],
    summary="List campaigns",
)
async def list_campaigns(
    current_user: CurrentUser,
    service: CampaignService = Depends(get_campaign_service),
) -> list[CampaignResponse]:
    """List all campaigns for the school."""
    return await service.list_by_school(school_id=UUID(current_user["school_id"]))


@router.patch(
    "/campaigns/{campaign_id}",
    response_model=CampaignResponse,
    summary="Update a campaign",
)
async def update_campaign(
    campaign_id: UUID,
    data: CampaignUpdate,
    current_user: CurrentUser,
    service: CampaignService = Depends(get_campaign_service),
) -> CampaignResponse:
    """Update a campaign."""
    try:
        return await service.update(
            campaign_id=campaign_id,
            data=data,
            school_id=UUID(current_user["school_id"]),
            user_id=UUID(current_user["sub"]),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.delete(
    "/campaigns/{campaign_id}",
    summary="Delete a campaign",
)
async def delete_campaign(
    campaign_id: UUID,
    current_user: CurrentUser,
    service: CampaignService = Depends(get_campaign_service),
) -> dict:
    """Delete a campaign."""
    campaign = await service.get_by_id(
        campaign_id=campaign_id,
        school_id=UUID(current_user["school_id"]),
    )
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found",
        )
    await service.delete(campaign_id)
    return {"message": "Campaign deleted"}


@router.post(
    "/campaigns/{campaign_id}/donate",
    response_model=DonationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Make a donation",
)
async def donate_to_campaign(
    campaign_id: UUID,
    data: DonationCreate,
    current_user: CurrentUser,
    service: DonationService = Depends(get_donation_service),
) -> DonationResponse:
    """Make a donation to a campaign."""
    try:
        return await service.create(
            data=data,
            user_id=UUID(current_user["sub"]),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/campaigns/{campaign_id}/donations",
    response_model=list[DonationResponse],
    summary="List donations for a campaign",
)
async def list_campaign_donations(
    campaign_id: UUID,
    current_user: CurrentUser,
    service: DonationService = Depends(get_donation_service),
) -> list[DonationResponse]:
    """List all donations for a campaign."""
    return await service.list_by_campaign(campaign_id=campaign_id)
