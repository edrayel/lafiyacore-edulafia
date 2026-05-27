"""Payroll service for business logic operations."""

from collections.abc import Sequence
from uuid import UUID

from edulafia.modules.payroll.repository import PayrollEntryRepository, PayrollRunRepository
from edulafia.modules.payroll.schemas import (
    PayrollEntryCreate,
    PayrollEntryResponse,
    PayrollEntryUpdate,
    PayrollRunCreate,
    PayrollRunResponse,
    PayrollRunUpdate,
)


class PayrollRunService:
    """Service for payroll run business logic."""

    def __init__(self, repository: PayrollRunRepository):
        self.repository = repository

    async def create(self, data: PayrollRunCreate, user_id: UUID) -> PayrollRunResponse:
        """Create a new payroll run."""
        run_data = data.model_dump()
        run = await self.repository.create(run_data)
        return PayrollRunResponse.model_validate(run)

    async def get_by_id(self, run_id: UUID, school_id: UUID) -> PayrollRunResponse | None:
        """Get a payroll run by ID."""
        run = await self.repository.get_by_id_and_school(run_id, school_id)
        if run:
            return PayrollRunResponse.model_validate(run)
        return None

    async def list_by_school(self, school_id: UUID) -> Sequence[PayrollRunResponse]:
        """List all payroll runs for a school."""
        runs = await self.repository.list_by_school(school_id)
        return [PayrollRunResponse.model_validate(r) for r in runs]

    async def update(self, run_id: UUID, data: PayrollRunUpdate, school_id: UUID, user_id: UUID) -> PayrollRunResponse:
        """Update a payroll run."""
        run = await self.repository.get_by_id_and_school(run_id, school_id)
        if not run:
            raise ValueError(f"Payroll run {run_id} not found")

        update_data = data.model_dump(exclude_none=True)
        updated_run = await self.repository.update(run, update_data)
        return PayrollRunResponse.model_validate(updated_run)

    async def approve(self, run_id: UUID, school_id: UUID) -> PayrollRunResponse:
        """Approve a payroll run."""
        run = await self.repository.get_by_id_and_school(run_id, school_id)
        if not run:
            raise ValueError(f"Payroll run {run_id} not found")
        if run.status != "draft":
            raise ValueError("Only draft payroll runs can be approved")

        update_data = {"status": "approved"}
        updated_run = await self.repository.update(run, update_data)
        return PayrollRunResponse.model_validate(updated_run)

    async def mark_paid(self, run_id: UUID, school_id: UUID) -> PayrollRunResponse:
        """Mark a payroll run as paid."""
        run = await self.repository.get_by_id_and_school(run_id, school_id)
        if not run:
            raise ValueError(f"Payroll run {run_id} not found")
        if run.status != "approved":
            raise ValueError("Only approved payroll runs can be marked as paid")

        update_data = {"status": "paid"}
        updated_run = await self.repository.update(run, update_data)
        return PayrollRunResponse.model_validate(updated_run)


class PayrollEntryService:
    """Service for payroll entry business logic."""

    def __init__(self, repository: PayrollEntryRepository):
        self.repository = repository

    async def create(self, data: PayrollEntryCreate, user_id: UUID) -> PayrollEntryResponse:
        """Create a new payroll entry."""
        entry_data = data.model_dump()
        entry = await self.repository.create(entry_data)
        return PayrollEntryResponse.model_validate(entry)

    async def get_by_id(self, entry_id: UUID) -> PayrollEntryResponse | None:
        """Get a payroll entry by ID."""
        entry = await self.repository.get_by_id(entry_id)
        if entry:
            return PayrollEntryResponse.model_validate(entry)
        return None

    async def list_by_payroll_run(self, payroll_run_id: UUID) -> Sequence[PayrollEntryResponse]:
        """List all entries for a payroll run."""
        entries = await self.repository.list_by_payroll_run(payroll_run_id)
        return [PayrollEntryResponse.model_validate(e) for e in entries]

    async def update(self, entry_id: UUID, data: PayrollEntryUpdate, school_id: UUID, user_id: UUID) -> PayrollEntryResponse:
        """Update a payroll entry."""
        entry = await self.repository.get_by_id_and_school(entry_id, school_id)
        if not entry:
            raise ValueError(f"Payroll entry {entry_id} not found")

        update_data = data.model_dump(exclude_none=True)
        updated_entry = await self.repository.update(entry, update_data)
        return PayrollEntryResponse.model_validate(updated_entry)
