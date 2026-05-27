"""Fundraising service for business logic operations."""

from collections.abc import Sequence
from uuid import UUID

from edulafia.modules.fundraising.repository import CampaignRepository, DonationRepository
from edulafia.modules.fundraising.schemas import (
    CampaignCreate,
    CampaignResponse,
    CampaignUpdate,
    DonationCreate,
    DonationResponse,
)


class CampaignService:
    """Service for campaign business logic."""

    def __init__(self, repository: CampaignRepository):
        self.repository = repository

    async def create(self, data: CampaignCreate, user_id: UUID) -> CampaignResponse:
        """Create a new campaign."""
        campaign_data = data.model_dump()
        campaign = await self.repository.create(campaign_data)
        return CampaignResponse.model_validate(campaign)

    async def get_by_id(self, campaign_id: UUID, school_id: UUID) -> CampaignResponse | None:
        """Get a campaign by ID."""
        campaign = await self.repository.get_by_id_and_school(campaign_id, school_id)
        if campaign:
            return CampaignResponse.model_validate(campaign)
        return None

    async def list_by_school(self, school_id: UUID) -> Sequence[CampaignResponse]:
        """List all campaigns for a school."""
        campaigns = await self.repository.list_by_school(school_id)
        return [CampaignResponse.model_validate(c) for c in campaigns]

    async def update(self, campaign_id: UUID, data: CampaignUpdate, school_id: UUID, user_id: UUID) -> CampaignResponse:
        """Update a campaign."""
        campaign = await self.repository.get_by_id_and_school(campaign_id, school_id)
        if not campaign:
            raise ValueError(f"Campaign {campaign_id} not found")

        update_data = data.model_dump(exclude_none=True)
        updated_campaign = await self.repository.update(campaign, update_data)
        return CampaignResponse.model_validate(updated_campaign)



    async def delete(self, campaign_id: UUID) -> None:
        """Delete a record."""
        record = await self.repository.get_by_id(campaign_id)
        if not record:
            raise ValueError(f"Record not found")
        await self.repository.delete(record)
class DonationService:
    """Service for donation business logic."""

    def __init__(self, repository: DonationRepository):
        self.repository = repository

    async def create(self, data: DonationCreate, user_id: UUID) -> DonationResponse:
        """Create a new donation."""
        donation_data = data.model_dump()
        donation = await self.repository.create(donation_data)
        return DonationResponse.model_validate(donation)

    async def get_by_id(self, donation_id: UUID) -> DonationResponse | None:
        """Get a donation by ID."""
        donation = await self.repository.get_by_id(donation_id)
        if donation:
            return DonationResponse.model_validate(donation)
        return None

    async def list_by_campaign(self, campaign_id: UUID) -> Sequence[DonationResponse]:
        """List all donations for a campaign."""
        donations = await self.repository.list_by_campaign(campaign_id)
        return [DonationResponse.model_validate(d) for d in donations]
