from __future__ import annotations
"""Fundraising repository for data access operations."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from edulafia.modules.fundraising.models import Campaign, Donation


class CampaignRepository:
    """Repository for campaign database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> Campaign:
        """Create a new campaign."""
        campaign = Campaign(**data)
        self.db.add(campaign)
        await self.db.flush()
        await self.db.refresh(campaign)
        return campaign

    async def get_by_id(self, campaign_id: UUID) -> Campaign | None:
        """Get a campaign by ID."""
        stmt = select(Campaign).where(Campaign.id == campaign_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id_and_school(self, campaign_id: UUID, school_id: UUID) -> Campaign | None:
        """Get a campaign by ID scoped to school."""
        stmt = select(Campaign).where(
            Campaign.id == campaign_id,
            Campaign.school_id == school_id,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_school(self, school_id: UUID) -> Sequence[Campaign]:
        """List all campaigns for a school."""
        stmt = select(Campaign).where(
            Campaign.school_id == school_id
        ).order_by(Campaign.start_date.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(self, campaign: Campaign, data: dict) -> Campaign:
        """Update a campaign."""
        for key, value in data.items():
            if value is not None:
                setattr(campaign, key, value)
        await self.db.flush()
        await self.db.refresh(campaign)
        return campaign

    async def delete(self, campaign: Campaign) -> None:
        """Delete a campaign."""
        await self.db.delete(campaign)
        await self.db.flush()


class DonationRepository:
    """Repository for donation database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> Donation:
        """Create a new donation."""
        donation = Donation(**data)
        self.db.add(donation)
        await self.db.flush()
        await self.db.refresh(donation)
        return donation

    async def get_by_id(self, donation_id: UUID) -> Donation | None:
        """Get a donation by ID."""
        stmt = select(Donation).where(Donation.id == donation_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_campaign(self, campaign_id: UUID) -> Sequence[Donation]:
        """List all donations for a campaign."""
        stmt = select(Donation).where(
            Donation.campaign_id == campaign_id
        ).order_by(Donation.date.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(self, donation: Donation, data: dict) -> Donation:
        """Update a donation."""
        for key, value in data.items():
            if value is not None:
                setattr(donation, key, value)
        await self.db.flush()
        await self.db.refresh(donation)
        return donation

    async def delete(self, donation: Donation) -> None:
        """Delete a donation."""
        await self.db.delete(donation)
        await self.db.flush()
